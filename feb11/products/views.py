from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .models import Product, Comment
from .serializer import (
    ProductSerializer,
    ProductCreateUpdateSerializer,
    CommentSerializer,
    CommentCreateSerializer,
)


class ProductListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Product.objects.filter(is_deleted=False)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductCreateUpdateSerializer
        return ProductSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Product.objects.filter(is_deleted=False)

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return ProductCreateUpdateSerializer
        return ProductSerializer

    def _ensure_owner(self, product):
        if not self.request.user or not self.request.user.is_authenticated:
            raise PermissionDenied("Authentication required")
        if product.owner_id != self.request.user.id:
            raise PermissionDenied("You do not own this product")

    def update(self, request, *args, **kwargs):
        product = self.get_object()
        self._ensure_owner(product)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        self._ensure_owner(product)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductSearchAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = Product.objects.filter(is_deleted=False)
        query = self.request.query_params.get("q", "").strip()
        if not query:
            return queryset
        return queryset.filter(Q(name__icontains=query) | Q(description__icontains=query))


class ProductCommentsListCreateAPIView(generics.ListCreateAPIView):
    def get_queryset(self):
        return Comment.objects.filter(
            is_deleted=False,
            product_id=self.kwargs["pk"],
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CommentCreateSerializer
        return CommentSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        product = get_object_or_404(
            Product.objects.filter(is_deleted=False),
            pk=self.kwargs["pk"],
        )
        serializer.save(user=self.request.user, product=product)


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Comment.objects.filter(is_deleted=False)

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH", "DELETE"):
            return [IsAuthenticated()]
        return [AllowAny()]

    def _ensure_owner(self, comment):
        if comment.user_id != self.request.user.id:
            raise PermissionDenied("You do not own this comment")

    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        self._ensure_owner(comment)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        self._ensure_owner(comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentsListAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Comment.objects.filter(is_deleted=False)
        return queryset