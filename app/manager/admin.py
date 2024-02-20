from django.contrib import admin
from helpers.models.baseadmin_model import AdminBaseModel
from manager.models import Page, Component, ComponentSection, Section

# Register your models here.


@admin.register(Component)
class ComponentAdmin(AdminBaseModel):
    list_display = ("id", "iid", "name", "is_active")
    search_fields = ("name",)


@admin.register(Page)
class TemplateAdmin(AdminBaseModel):
    list_display = ("id", "iid", "name", "page_route", "is_active")
    ordering = ("created_at",)
    search_fields = ("name",)


@admin.register(Section)
class SectionAdmin(AdminBaseModel):
    list_display = ("id", "iid", "name", "is_active")


@admin.register(ComponentSection)
class ComponentSectionAdmin(AdminBaseModel):
    list_display = ("id", "iid", "component", "section", "is_active")
