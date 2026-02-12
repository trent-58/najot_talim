from rest_framework import serializers
from .models import Product, Comment


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = (
            "id",
            "owner",
            "name",
            "price",
            "description",
            "created_at",
            "updated_at",
        )


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("name", "price", "description")


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ("id", "product", "user", "comment", "created_at", "updated_at")
        read_only_fields = ("id", "product", "user", "created_at", "updated_at")


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("comment",)
