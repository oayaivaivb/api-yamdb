from django.urls import path

from .views import ReviewViewSet, CommentViewSet

review_list = ReviewViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

review_detail = ReviewViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})

comment_list = CommentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

comment_detail = CommentViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path(
        'titles/<int:title_id>/reviews/',
        review_list,
        name='review-list'
    ),
    path(
        'titles/<int:title_id>/reviews/<int:pk>/',
        review_detail,
        name='review-detail'
    ),
    path(
        'titles/<int:title_id>/reviews/<int:review_id>/comments/',
        comment_list,
        name='comment-list'
    ),
    path(
        'titles/<int:title_id>/reviews/<int:review_id>/comments/<int:pk>/',
        comment_detail,
        name='comment-detail'
    ),
]
