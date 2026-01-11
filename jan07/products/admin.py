from django.contrib import admin
from .models import Car


class CarAdmin(admin.ModelAdmin):
    list_display = ("make", "model", "year", "price", "color")
    search_fields = ("make", "model", "year", "color")
    list_filter = ("year", "price", "color")


admin.site.register(Car, CarAdmin)
