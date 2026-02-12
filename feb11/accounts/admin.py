from django.contrib import admin
from baseapp.admin import BaseAdmin
from accounts.models import User

@admin.register(User)
class UserAdmin(BaseAdmin):
    pass
