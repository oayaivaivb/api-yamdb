<<<<<<< HEAD
from django.shortcuts import render

# Create your views here.
=======
from rest_framework import viewsets

from .models import Review, Comment
from .serializers import ReviewSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title=title_id)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user.id,
            title=self.kwargs.get('title_id')
        )

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        return Comment.objects.filter(review_id=review_id)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user.id,
            review_id=self.kwargs.get('review_id')
        )
>>>>>>> f9b892d (отзывы и комменты с заглушками)
