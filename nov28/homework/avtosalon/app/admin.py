from django.contrib import admin

# Register your models here.
from .models import Product, User, Order

admin.site.register(Product)
admin.site.register(User)
admin.site.register(Order)