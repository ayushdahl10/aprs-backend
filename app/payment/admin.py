from django.contrib import admin
from helpers.models.baseadmin_model import AdminBaseModel
from payment.models import PaymentMethod

# Register your models here.


@admin.register(PaymentMethod)
class PaymentMethodAdmin(AdminBaseModel):
    list_display = [
        "name",
        "is_active",
        "enable_sandbox",
        "is_deleted",
    ]
