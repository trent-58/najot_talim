from django.contrib import admin
from .models import Category, Product
from .forms import ProductForm


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name", "description")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("name", "description")
    autocomplete_fields = ("category",)
    readonly_fields = ("created_at", "updated_at")
    form = ProductForm
