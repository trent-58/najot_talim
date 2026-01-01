from django.contrib import admin
from . import models


class CartItemInline(admin.TabularInline):
    model = models.CartItem
    extra = 0


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_key', 'total_items', 'created_at']
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_sku', 'quantity', 'price', 'total_price']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'email', 'status', 'total', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'email', 'last_name']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]


admin.site.register(models.Cart, CartAdmin)
admin.site.register(models.Order, OrderAdmin)


