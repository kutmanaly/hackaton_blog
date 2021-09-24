from django_filters import rest_framework as rest_filters
from rest_framework import viewsets, mixins, filters
from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import GenericViewSet
from post.models import Post, Comment, Like
from post.permissions import IsAuthor, IsAuthorOrIsAdmin
from post.serializers import (PostListSerializer,
                              PostDetailSerializer,
                              CreatePostSerializer,
                              CommentSerializer)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action


class PostFilter(rest_filters.FilterSet):
    created_at = rest_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Post
        fields = ('title', 'created_at')


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = CreatePostSerializer
    permission_classes = [IsAuthorOrIsAdmin]
    filter_backends = [rest_filters.DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_class = PostFilter
    search_fields = ['title', 'text']
    ordering_fields = ['created_at', 'title']

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        elif self.action == 'retrieve':
            return PostDetailSerializer
        return CreatePostSerializer

    @action(['POST'], detail=True)
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(post=post, user=user)
            like.is_liked = not like.is_liked
            like.save()
            message = 'нравится' if like.is_liked else 'не нравится'
        except Like.DoesNotExist:
            Like.objects.create(post=post, user=user, is_liked=True)
            message = 'нравится'
        return Response(message, status=200)


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAuthor()]


class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class CreatePostView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class UpdatePostView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class DeletePostView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


