from django.contrib import admin
from baseapp.admin import BaseAdmin
from orders.models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(BaseAdmin):
    pass


@admin.register(OrderItem)
class OrderItemAdmin(BaseAdmin):
    pass
