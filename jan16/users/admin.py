from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
  list_display = ['first_name', 'last_name', 'username', 'phone', 'address']

admin.site.register(CustomUser, CustomUserAdmin)