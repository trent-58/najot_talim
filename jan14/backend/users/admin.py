from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "username", "language")
    search_fields = ("first_name", "last_name", "username")
    list_filter = ("language",)
    ordering = ("-date_joined",)

    # Each entry must be (name, dict). The dict must contain a "fields" key.
    fieldsets = (
        ("Basic Info", {"fields": ("first_name", "last_name", "username", "password")}),
        ("Preferences", {"fields": ("language", "email")}),

    )


# Optional: remove Group from admin UI
admin.site.unregister(Group)
