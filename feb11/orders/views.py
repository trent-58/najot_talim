from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, PermissionDenied

from .models import Order, OrderItem
from .serializer import OrderSerializer, OrderStatusSerializer
from carts.views import get_or_create_active_cart


class OrderCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        cart = get_or_create_active_cart(request.user)
        items = cart.items.filter(is_deleted=False)
        if not items.exists():
            raise ValidationError("Cart is empty")
        order = Order.objects.create(user=request.user)
        order_items = [
            OrderItem(order=order, product=item.product, quantity=item.quantity)
            for item in items
        ]
        OrderItem.objects.bulk_create(order_items)
        cart.checked_out_at = timezone.now()
        cart.save(update_fields=["checked_out_at"])
        cart.delete()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderListAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_deleted=False)


class OrderDetailAPIView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_deleted=False)


class OrderStatusUpdateAPIView(APIView):
    permission_classes = (IsAdminUser,)

    def patch(self, request, pk):
        serializer = OrderStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = Order.objects.filter(id=pk, is_deleted=False).first()
        if order is None:
            raise ValidationError("Order not found")

        current_status = "pending"
        if order.is_paid:
            current_status = "paid"
        if order.delivered_at:
            current_status = "shipped"

        next_status = serializer.validated_data["status"]
        if current_status == "pending" and next_status not in ("pending", "paid"):
            raise ValidationError("Invalid status transition")
        if current_status == "paid" and next_status not in ("paid", "shipped"):
            raise ValidationError("Invalid status transition")
        if current_status == "shipped" and next_status != "shipped":
            raise ValidationError("Invalid status transition")

        if next_status == "pending":
            order.is_paid = False
            order.delivered_at = None
        elif next_status == "paid":
            order.is_paid = True
            order.delivered_at = None
        else:
            order.is_paid = True
            if order.delivered_at is None:
                order.delivered_at = timezone.now()
        order.save(update_fields=["is_paid", "delivered_at"])
        return Response(OrderSerializer(order).data)


class OrderCancelAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, pk):
        order = Order.objects.filter(id=pk, is_deleted=False).first()
        if order is None:
            raise ValidationError("Order not found")
        if order.user_id != request.user.id:
            raise PermissionDenied("You do not own this order")
        if order.delivered_at:
            raise ValidationError("Shipped orders cannot be canceled")
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
