from django.db import models
from helpers.models.base_model import BaseModel
from helpers.mixins.constant import WEBSITE_IID_PAYMENT_METHOD, WEBSITE_IID_PAYMENT_LOGS
from payment.constant import PaymentStatus
from website.TextChoices import SubscriptionType


# Create your models here.
class PaymentMethod(BaseModel):
    IID_PREFIX_KEY = WEBSITE_IID_PAYMENT_METHOD
    name = models.CharField(max_length=125, unique=True, null=False, blank=True)
    enable_sandbox = models.BooleanField(default=False)
    config = models.JSONField(default={}, blank=True)
    schema = models.JSONField(default={}, blank=True)

    def delete(self, force=True, *args, **kwargs):
        return super().delete(force, *args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name}"


class PaymentLog(BaseModel):
    IID_PREFIX_KEY = WEBSITE_IID_PAYMENT_LOGS
    transaction = models.ForeignKey(
        "payment.TransactionLog", on_delete=models.PROTECT, null=True
    )
    subscription_type = models.CharField(
        choices=SubscriptionType.choices, null=False, default=SubscriptionType.MONTHLY
    )
    payment_datetime = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return f"{self.iid}=>{self.transaction.transaction_code}"
