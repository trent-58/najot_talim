from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product


class ProductSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "price")


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSummarySerializer()

    class Meta:
        model = OrderItem
        fields = ("id", "product", "quantity", "created_at", "updated_at")


class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "is_paid",
            "delivered_at",
            "items",
            "created_at",
            "updated_at",
        )

    def get_items(self, obj):
        items = obj.items.filter(is_deleted=False)
        return OrderItemSerializer(items, many=True).data

    def get_status(self, obj):
        if obj.delivered_at:
            return "shipped"
        if obj.is_paid:
            return "paid"
        return "pending"


class OrderStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=("pending", "paid", "shipped"))
