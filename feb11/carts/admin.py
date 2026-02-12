from django.contrib import admin
from baseapp.admin import BaseAdmin
from carts.models import Cart, CartItem

@admin.register(Cart)
class CartAdmin(BaseAdmin):
    pass


@admin.register(CartItem)
class CartItemAdmin(BaseAdmin):
    pass
