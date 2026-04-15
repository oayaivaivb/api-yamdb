"""Модуль представлений (views) для API приложения."""

from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets, filters, mixins
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from reviews.models import User, Review, Comment, Category, Genre, Title
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrModeratorOrAdmin
from .serializers import (
    SignUpSerializer,
    TokenSerializer,
    UserSerializer,
    ReviewSerializer,
    CommentSerializer,
    GenreSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    CategorySerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Регистрация нового пользователя и отправка кода подтверждения."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    """Получение JWT токена по username и confirmation_code."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'token': serializer.validated_data['token']})


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для управления пользователями (только для админов)."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_permissions(self):
        """Назначение прав доступа в зависимости от действия."""
        if self.action == 'me':
            return (IsAuthenticated(),)
        return (IsAdmin(),)

    @action(detail=False, methods=['get', 'patch', 'delete'], url_path='me')
    def me(self, request):
        """Получение, обновление данных текущего пользователя."""
        user = request.user

        if request.method == 'DELETE':
            return Response(
                {'detail': 'Method DELETE not allowed'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        # PATCH запрос
        data = request.data.copy()
        data.pop('role', None)
        serializer = self.get_serializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для управления отзывами на произведения."""

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrModeratorOrAdmin]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для управления комментариями к отзывам."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrModeratorOrAdmin]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))


    def get_queryset(self):
        return self.get_review().comments.all()


    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
    )

class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Базовый вьюсет для категорий и жанров."""
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    """ViewSet для управления категориями."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(ListCreateDestroyViewSet):
    """ViewSet для управления жанрами."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для управления произведениями."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = TitleWriteSerializer

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия."""
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer

    def get_queryset(self):
        """Фильтрация произведений по параметрам запроса."""
        queryset = super().get_queryset()

        # Фильтрация по жанру
        genre_slug = self.request.query_params.get('genre')
        if genre_slug:
            queryset = queryset.filter(genre__slug=genre_slug)

        # Фильтрация по категории
        category_slug = self.request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Фильтрация по году
        year = self.request.query_params.get('year')
        if year:
            queryset = queryset.filter(year=year)

        # Поиск по имени
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset
