from django_filters import rest_framework as rest_filters
from rest_framework import viewsets, mixins, filters
from rest_framework.viewsets import GenericViewSet
from post.models import Product, Comment, Like
from post.permissions import IsAuthor, IsAuthorOrIsAdmin
from post.serializer import (ProductListSerializer,
                             ProductDetailSerializer,
                             CreateProductSerializer,
                             CommentSerializer)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action


class ProductFilter(rest_filters.FilterSet):
    created_at = rest_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Product
        fields = ('title', 'created_at')


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = CreateProductSerializer
    permission_classes = [IsAuthorOrIsAdmin]
    filter_backends = [rest_filters.DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'text']
    ordering_fields = ['created_at', 'title']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action == 'retrieve':
            return ProductDetailSerializer
        return CreateProductSerializer

    @action(['POST'], detail=True)
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(post=post, user=user)
            like.is_liked = not like.is_liked
            like.save()
            message = 'нравится' if like.is_liked else 'ненравится'
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



