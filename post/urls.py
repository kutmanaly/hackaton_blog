from django.db import router
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (PostViewSet,
                    CommentViewSet, PostDetailView, CreatePostView, DeletePostView, UpdatePostView)


router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('comments', CommentViewSet)

urlpatterns = [
    path('posts', PostViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('comments', CommentViewSet.as_view({'get': 'list', 'post': 'create'})),
]
urlpatterns += router.urls


# urlpatterns = [
#     path('posts/', PostViewSet.as_view({'get': 'list'})),
#     path('posts/<int:pk>/', PostDetailView.as_view(), name='post_details'),
#     path('posts/create/', CreatePostView.as_view(), name='create_post'),
#     path('posts/delete/<int:pk>/', DeletePostView.as_view(), name='delete_post'),
#     path('posts/update/<int:pk>/', UpdatePostView.as_view(), name='update_post'),
# ]