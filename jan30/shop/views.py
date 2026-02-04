from decimal import Decimal
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Product, Cart, CartItem, Order, OrderItem
from .serializers import ProductSerializer, CartSerializer, OrderSerializer


class ProductListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        qs = Product.objects.filter(is_active=True).order_by("id")
        return Response(ProductSerializer(qs, many=True).data)


def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = get_or_create_cart(request.user)
        return Response(CartSerializer(cart).data)


class CartAddItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = get_or_create_cart(request.user)
        product_id = request.data.get("product_id")
        qty = int(request.data.get("quantity", 1))

        if not product_id or qty <= 0:
            return Response({"detail": "product_id and positive quantity required"}, status=400)

        product = Product.objects.filter(id=product_id, is_active=True).first()
        if not product:
            return Response({"detail": "Product not found"}, status=404)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={"quantity": qty})
        if not created:
            item.quantity += qty
            item.save(update_fields=["quantity"])

        return Response(CartSerializer(cart).data, status=200)


class CartUpdateItemView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, item_id: int):
        cart = get_or_create_cart(request.user)
        item = CartItem.objects.filter(cart=cart, id=item_id).first()
        if not item:
            return Response({"detail": "Item not found"}, status=404)

        qty = int(request.data.get("quantity", item.quantity))
        if qty <= 0:
            item.delete()
        else:
            item.quantity = qty
            item.save(update_fields=["quantity"])

        return Response(CartSerializer(cart).data, status=200)


class CartClearView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = get_or_create_cart(request.user)
        cart.items.all().delete()
        return Response(CartSerializer(cart).data, status=200)


class CheckoutCreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        cart = get_or_create_cart(request.user)
        items = list(cart.items.select_related("product").all())

        if not items:
            return Response({"detail": "Cart is empty"}, status=400)

        order = Order.objects.create(user=request.user)

        subtotal = Decimal("0.00")
        for ci in items:
            unit_price = ci.product.price
            OrderItem.objects.create(
                order=order,
                product=ci.product,
                quantity=ci.quantity,
                unit_price=unit_price,
            )
            subtotal += unit_price * ci.quantity

        order.subtotal = subtotal
        order.total = subtotal  # later: taxes, shipping, discounts
        order.save(update_fields=["subtotal", "total"])

        cart.items.all().delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class MyOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Order.objects.filter(user=request.user).order_by("-id").prefetch_related("items__product")
        return Response(OrderSerializer(qs, many=True).data)
