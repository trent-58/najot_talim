from django.contrib import admin

# Register your models here.
from .models import Item, Category, Manufacturer

admin.site.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'manufacturer', 'price', 'stock')
    search_fields = ('name', 'category__name', 'manufacturer__name')
    list_filter = ('category', 'manufacturer')


admin.site.register(Category)
admin.site.register(Manufacturer)