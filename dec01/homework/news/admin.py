from django.contrib import admin

# Register your models here.
from .models import category, news

admin.site.register(category)
admin.site.register(news)
