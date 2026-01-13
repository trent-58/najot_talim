from django.contrib import admin
from .models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("brand", "model", "year", "price", "color", "mileage")
    list_filter = ("brand", "year", "color")
    search_fields = ("brand", "model", "color")
    ordering = ("-created_at",)
