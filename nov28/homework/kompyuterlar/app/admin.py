from django.contrib import admin

# Register your models here.
from .models import order, user, laptop

admin.site.register(order)
admin.site.register(user)
admin.site.register(laptop)
