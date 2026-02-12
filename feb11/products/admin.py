from django.contrib import admin
from baseapp.admin import BaseAdmin
from products.models import Comment, Product

@admin.register(Product)
class ProductAdmin(BaseAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(BaseAdmin):
    pass
