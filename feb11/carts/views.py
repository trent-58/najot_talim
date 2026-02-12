from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from .models import Cart, CartItem
from .serializer import (
    CartSerializer,
    CartAddSerializer,
    CartUpdateSerializer,
    CartRemoveSerializer,
)
from products.models import Product


def get_or_create_active_cart(user):
    cart = Cart.objects.filter(
        user=user,
        checked_out_at__isnull=True,
        is_deleted=False,
    ).first()
    if cart is None:
        cart = Cart.objects.create(user=user)
    return cart


class CartDetailAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        cart = get_or_create_active_cart(request.user)
        return Response(CartSerializer(cart).data)


class CartAddAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = CartAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = get_or_create_active_cart(request.user)
        product = Product.objects.get(id=serializer.validated_data["product_id"])
        quantity = serializer.validated_data["quantity"]
        item = CartItem.objects.filter(
            cart=cart,
            product=product,
            is_deleted=False,
        ).first()
        if item is None:
            CartItem.objects.create(cart=cart, product=product, quantity=quantity)
        else:
            item.quantity += quantity
            item.save(update_fields=["quantity"])
        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)


class CartRemoveAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = CartRemoveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = get_or_create_active_cart(request.user)
        item = CartItem.objects.filter(
            cart=cart,
            product_id=serializer.validated_data["product_id"],
            is_deleted=False,
        ).first()
        if item is None:
            raise ValidationError("Product not in cart")
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartClearAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        cart = get_or_create_active_cart(request.user)
        cart.items.filter(is_deleted=False).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartUpdateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request):
        serializer = CartUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = get_or_create_active_cart(request.user)
        item = CartItem.objects.filter(
            cart=cart,
            product_id=serializer.validated_data["product_id"],
            is_deleted=False,
        ).first()
        if item is None:
            raise ValidationError("Product not in cart")
        item.quantity = serializer.validated_data["quantity"]
        item.save(update_fields=["quantity"])
        return Response(CartSerializer(cart).data)
