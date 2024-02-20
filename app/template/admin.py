from django.contrib import admin
from template.models import TemplateManager
from helpers.models.baseadmin_model import AdminBaseModel

# Register your models here.


@admin.register(TemplateManager)
class TemplateManagerAdmin(AdminBaseModel):
    list_display = ("id", "iid", "name")
    search_fields = ("name",)
