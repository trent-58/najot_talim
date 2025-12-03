from django.contrib import admin

from .models import category, meal

admin.site.register(category)
admin.site.register(meal)