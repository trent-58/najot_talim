from django.contrib import admin
from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "published_at", "is_published")
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("is_published", "category")
    search_fields = ("title", "excerpt", "content")
