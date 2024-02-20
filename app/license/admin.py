from django.contrib import admin

from helpers.models.baseadmin_model import AdminBaseModel
from license.models import License, Client, Subscription


@admin.register(License)
class LicenseAdmin(AdminBaseModel):
    list_display = ["iid", "client", "license_key", "start_date", "end_date", "status"]
    readonly_fields = [
        "license_key",
        "created_at",
        "created_by",
        "is_deleted",
        "updated_by",
    ]


@admin.register(Client)
class ClientAdmin(AdminBaseModel):
    list_display = ["iid", "name", "contact", "is_active"]


@admin.register(Subscription)
class SubscriptionAdmin(AdminBaseModel):
    list_display = ["iid", "name", "is_active", "billing_type"]
