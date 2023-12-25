from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget
from django.forms import DateTimeField, SplitDateTimeWidget
from django.db import models

# Register your models here.


class AdminBaseModel(admin.ModelAdmin):
    readonly_fields = ["created_at", "created_by", "is_deleted", "updated_by"]
    list_display = ["iid", "created_by", "created_at", "is_deleted", "is_active"]

    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
        DateTimeField: {
            "widget": SplitDateTimeWidget(
                date_attrs={
                    "type": "date",
                    "class": "vDateField mr-2",
                },
                time_attrs={"type": "time", "class": "vTimeField"},
            )
        },
    }

    def save_model(self, request, obj, form, change):
        if obj.created_by:
            obj.updated_by = str(request.user)
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
