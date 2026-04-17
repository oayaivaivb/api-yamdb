"""Модуль сериализаторов для API приложения."""

import string
import random

from django.core.mail import send_mail
from django.conf import settings
from django.db import IntegrityError

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers

from reviews.models import User, Review, Comment, Category, Genre, Title


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователя."""

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
        required=True,
        error_messages={'invalid': 'Username содержит недопустимые символы.'}
    )
    email = serializers.EmailField(max_length=254)

    @staticmethod
    def generate_code():
        """Генерация случайного кода подтверждения."""
        return ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=6
        ))

    def send_confirmation_email(self, user):
        """Отправка письма с кодом подтверждения."""
        send_mail(
            subject='Код подтверждения YaMDb',
            message=f'Ваш код подтверждения: {user.confirmation_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

    def validate_username(self, value):
        """Валидация username."""
        if value == 'me':
            raise serializers.ValidationError(
                'Имя "me" использовать запрещено.'
            )
        return value

    def create(self, validated_data):
        """Создание пользователя."""
        username = validated_data['username']
        email = validated_data['email']
        user = self.get_or_create_user(username, email)
        self.send_confirmation_email(user)
        return {'username': user.username, 'email': user.email}

    def get_or_create_user(self, username, email):
        """Получение или создание пользователя."""
        code = self.generate_code()
        try:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': email, 'confirmation_code': code}
            )
            if not created:
                if user.email != email:
                    raise serializers.ValidationError({
                        'email': 'Email не совпадает с зарегистрированным'
                    })
                user.confirmation_code = code
                user.save(update_fields=['confirmation_code'])
            else:
                user.set_unusable_password()
                user.save(update_fields=['password'])
            return user
        except IntegrityError:
            raise serializers.ValidationError({
                'email': 'Пользователь с таким email уже существует.'
            })


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения JWT токена."""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=6)

    def validate(self, data):
        """Валидация кода подтверждения."""
        user = self.context.get('user')
        if not user:
            raise serializers.ValidationError(
                'Пользователь не передан в контекст.'
            )

        if data.get('confirmation_code') != user.confirmation_code:
            raise serializers.ValidationError(
                'Неверный код подтверждения.'
            )

        user.confirmation_code = ''
        user.save(update_fields=['confirmation_code'])
        refresh = RefreshToken.for_user(user)
        return {'token': str(refresh.access_token)}


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_username(self, value):
        """Валидация username."""
        if value == 'me':
            raise serializers.ValidationError(
                'Имя "me" использовать запрещено.'
            )

        queryset = User.objects.filter(username=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует.'
            )
        return value

    def validate_email(self, value):
        """Валидация email."""
        queryset = User.objects.filter(email=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует.'
            )
        return value

    def create(self, validated_data):
        """Создание пользователя."""
        user = User(**validated_data)
        user.set_unusable_password()
        user.save()
        return user


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    author = serializers.StringRelatedField(read_only=True)
    title = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('id', 'pub_date')

    def validate_score(self, value):
        """Валидация оценки."""
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                'Оценка должна быть от 1 до 10'
            )
        return value

    def validate(self, data):
        request = self.context.get('request')

        if request.method != 'POST':
            return data

        title_id = request.parser_context.get('kwargs', {}).get('title_id')

        if Review.objects.filter(
            author=request.user,
            title_id=title_id
        ).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на это произведение'
            )

        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.StringRelatedField(read_only=True)
    review = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'pub_date')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения модели Title."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        read_only_fields = fields


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи модели Title."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )

    class Meta:
        model = Title
        fields = '__all__'

    def to_representation(self, instance):
        return TitleReadSerializer(instance, context=self.context).data
