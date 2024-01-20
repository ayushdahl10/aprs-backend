from django.contrib import admin
from helpers.models.baseadmin_model import AdminBaseModel
from payment.models import PaymentMethod, PaymentLog, TransactionLog

# Register your models here.


@admin.register(PaymentMethod)
class PaymentMethodAdmin(AdminBaseModel):
    list_display = [
        "name",
        "is_active",
        "enable_sandbox",
        "is_deleted",
    ]


@admin.register(PaymentLog)
class PaymentLogAdmin(AdminBaseModel):
    list_display = [
        "iid",
        "transaction",
        "subscription_type",
        "created_at",
    ]


@admin.register(TransactionLog)
class TransactionLogAdmin(AdminBaseModel):
    list_display = [
        "iid",
        "transaction_code",
        "amount",
        "expire_at",
    ]
