from django.shortcuts import render


from rest_framework import viewsets

from .models import Review, Comment
from .serializers import ReviewSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(
            title=self.kwargs.get('title_id')
        )

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user.id,
            title=self.kwargs.get('title_id')
        )

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(
            review=self.kwargs.get('review_id')
        )

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user.id,
            review=self.kwargs.get('review_id')
        )
