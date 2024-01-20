from django.db import models
from helpers.models.base_model import BaseModel
from helpers.mixins.constant import WEBSITE_IID_TRANSACTION_LOGS
from payment.constant import PaymentStatus
from helpers.mixins.helper import generate_random_string


class TransactionLog(BaseModel):
    IID_PREFIX_KEY = WEBSITE_IID_TRANSACTION_LOGS
    transaction_code = models.CharField(max_length=8, null=False, blank=True)
    license = models.ForeignKey("license.Client", on_delete=models.PROTECT, null=False)
    amount = models.IntegerField()
    status = models.CharField(
        choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    payment_method = models.ForeignKey(
        "payment.PaymentMethod", on_delete=models.PROTECT, null=True
    )
    expire_at = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return f"{self.transaction_code}"

    def save(self, *args, **kwargs):
        if not self.transaction_code:
            self.transaction_code = generate_random_string(8)
        return super().save(*args, **kwargs)
