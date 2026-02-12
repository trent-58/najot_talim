from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin

class BaseAdmin(admin.ModelAdmin):
    compressed_fields = True
    list_fullwidth = True
    list_actions = ('export_csv',)


try:
    admin.site.unregister(Group)
except NotRegistered:
    pass
