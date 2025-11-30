from django.contrib import admin

# Register your models here.
from .models import Order, User, Product

admin.site.register(Order)
admin.site.register(User)
admin.site.register(Product)