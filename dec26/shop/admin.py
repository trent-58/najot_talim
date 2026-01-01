from django.contrib import admin

from shop.models import Product, Category, ProductImage, Inventory


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'is_primary', 'position']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'sku', 'price', 'discount_price']
    inlines = [ProductImageInline]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'alt_text', 'is_primary', 'position']

class InventoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'stock_quantity', 'in_stock']

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Inventory, InventoryAdmin)

