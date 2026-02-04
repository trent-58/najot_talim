from django.contrib import admin
from .models import Product, Cart, CartItem, Order, OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "is_active")
    list_editable = ("price", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("id",)
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    autocomplete_fields = ("product",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "updated_at")
    search_fields = ("user__username", "user__email")
    inlines = (CartItemInline,)
    readonly_fields = ("created_at", "updated_at")

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    autocomplete_fields = ("product",)
    readonly_fields = ("unit_price",)
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "subtotal", "total", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "user__email")
    readonly_fields = ("subtotal", "total", "created_at")
    inlines = (OrderItemInline,)

    actions = ["mark_as_paid", "mark_as_shipped", "mark_as_canceled"]

    def mark_as_paid(self, request, queryset):
        queryset.update(status=Order.Status.PAID)

    def mark_as_shipped(self, request, queryset):
        queryset.update(status=Order.Status.SHIPPED)

    def mark_as_canceled(self, request, queryset):
        queryset.update(status=Order.Status.CANCELED)

    mark_as_paid.short_description = "Mark selected orders as PAID"
    mark_as_shipped.short_description = "Mark selected orders as SHIPPED"
    mark_as_canceled.short_description = "Mark selected orders as CANCELED"
