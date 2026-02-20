from django.contrib import admin

from .models import Experience, Profile, Project, Skill


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "role", "email", "location")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "level", "sort_order")
    list_filter = ("category",)
    search_fields = ("name", "category")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "featured", "tech_stack", "sort_order")
    list_filter = ("featured",)
    search_fields = ("title", "tech_stack")


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("company", "role", "period", "sort_order")
    search_fields = ("company", "role")
