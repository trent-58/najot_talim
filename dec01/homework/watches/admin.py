from django.contrib import admin

# Register your models here.
from .models import company, order, watch


admin.site.register(company)
admin.site.register(order)
admin.site.register(watch)