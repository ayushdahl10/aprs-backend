from django.db import models

from helpers.mixins.constant import (
    WEBSITE_IID_LICENSE,
    WEBSITE_IID_CLIENT,
)
from helpers.models.base_model import BaseModel
from website.TextChoices import LicenseStatus, LicenseType, BillingType
from helpers.mixins.helper import generate_random_string


class Subscription(BaseModel):
    name = models.CharField(max_length=100, unique=True, null=False, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=15, default=0.0)
    billing_type = models.CharField(
        choices=BillingType.choices, default=BillingType.MONTHLY
    )

    def __str__(self) -> str:
        return f"{self.name}=>{self.billing_type}"

    def get_basic_info(self):
        return {
            "iid": self.iid,
            "name": self.name,
            "price": self.price,
            "billing_type": self.billing_type.capitalize(),
        }


class Client(BaseModel):
    IID_PREFIX_KEY = WEBSITE_IID_CLIENT
    name = models.CharField(max_length=256, null=False, blank=True)
    email = models.EmailField(max_length=256, null=False, blank=True, unique=True)
    contact = models.CharField(
        max_length=20,
        null=False,
        blank=True,
        help_text="Enter clients contact number here",
    )
    country = models.CharField(max_length=256, null=False, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    userdetail = models.OneToOneField(
        "autho.UserDetail", on_delete=models.CASCADE, null=True
    )

    def __str__(self) -> str:
        return f"{self.name}"


# Create your models here.
class License(BaseModel):
    IID_PREFIX_KEY = WEBSITE_IID_LICENSE
    client = models.OneToOneField("license.Client", on_delete=models.PROTECT, null=True)
    subscription = models.ForeignKey(
        "license.Subscription", on_delete=models.PROTECT, null=True
    )
    license_key = models.CharField(
        unique=True,
        max_length=256,
        null=False,
        blank=False,
    )
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    grace_period = models.IntegerField(null=False, default=2, blank=True)
    status = models.CharField(
        choices=LicenseStatus.choices, default=LicenseStatus.INACTIVE, null=False
    )

    def __str__(self):
        return f"{self.license_key}"

    def save(self, *args, **kwargs):
        if not self.license_key:
            self.license_key = generate_random_string(18)
        return super().save(*args, **kwargs)

    def delete(self, force=True, *args, **kwargs):
        return super().delete(force, *args, **kwargs)
