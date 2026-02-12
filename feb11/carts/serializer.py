from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product


class ProductSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "price")


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSummarySerializer()

    class Meta:
        model = CartItem
        fields = ("id", "product", "quantity", "created_at", "updated_at")


class CartSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ("id", "items", "created_at", "updated_at")

    def get_items(self, obj):
        items = obj.items.filter(is_deleted=False)
        return CartItemSerializer(items, many=True).data


class CartAddSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, required=False, default=1)

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value, is_deleted=False).exists():
            raise serializers.ValidationError("Product not found")
        return value


class CartUpdateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value, is_deleted=False).exists():
            raise serializers.ValidationError("Product not found")
        return value


class CartRemoveSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value, is_deleted=False).exists():
            raise serializers.ValidationError("Product not found")
        return value
