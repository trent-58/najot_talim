from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone_number', 'user_status', 'auth_type']


admin.site.register(CustomUser, CustomUserAdmin)