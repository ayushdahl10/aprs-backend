from helpers.models.base_model import BaseModel
from django.db import models
from helpers.mixins.constant import WEBSITE_IID_PROPERTY
from property.constant import PaymentTypeChoices, LeaseStatus
from datetime import timedelta


class Tenant(BaseModel):
    user = models.ForeignKey(
        "autho.UserDetail",
        on_delete=models.PROTECT,
        help_text="One who borrows the property or place",
    )
    property = models.ForeignKey("property.Property", on_delete=models.CASCADE)
    title = models.CharField(
        max_length=256,
        null=False,
        blank=True,
        default="",
    )
    upload_document = models.FileField(
        upload_to="image/tenant/documents/", null=True, blank=True
    )
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f" {self.property.name} => {self.title}  "


class LeaseInformation(BaseModel):
    tenant = models.OneToOneField(
        "property.Tenant", on_delete=models.CASCADE, related_name="lease_information"
    )
    lease_type = models.CharField(
        choices=PaymentTypeChoices.choices, default=PaymentTypeChoices.MONTHLY
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Enter amount eg:1000"
    )
    tax = models.DecimalField(
        max_digits=5, decimal_places=2, help_text="enter tax percentage"
    )
    due_date = models.DateField(null=True, editable=False, verbose_name="billing date")
    lease_status = models.CharField(
        choices=LeaseStatus.choices, default=LeaseStatus.NOT_ACTIVE
    )

    def __str__(self):
        return f"Lease Information for {self.tenant}"

    def save(self, *args, **kwargs):
        if self.lease_status == LeaseStatus.ACTIVE:
            if self.lease_type == PaymentTypeChoices.MONTHLY:
                self.due_date = self.tenant.start_date + timedelta(weeks=4)
            elif self.lease_type == PaymentTypeChoices.WEEKLY:
                self.due_date = self.tenant.start_date + timedelta(days=7)
            elif self.lease_type == PaymentTypeChoices.YEARLY:
                self.due_date == self.tenant.start_date + timedelta(weeks=52)
        return super().save(*args, **kwargs)

    def delete(self, force=True, *args, **kwargs):
        return super().delete(force, *args, **kwargs)
