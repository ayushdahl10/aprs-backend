from django.db import models

from helpers.mixins.constant import (
    WEBSITE_IID_ADVANCE_SETTING,
    WEBSITE_IID_COMPANY_DETAIL,
    WEBSITE_IID_DEPARTMENT,
    WEBSITE_IID_TERMINAL,
)
from helpers.models.base_model import BaseModel


# Create your models here.


class Company(BaseModel):
    IID_PREFIX_KEY = WEBSITE_IID_COMPANY_DETAIL
    company_name = models.CharField(max_length=256, blank=True, null=False, unique=True)
    company_logo = models.ImageField(
        null=False,
        blank=True,
        upload_to="images/company/logo/",
    )
    country = models.CharField(max_length=256, null=False, blank=True)
    address = models.CharField(max_length=126, null=False, blank=True)
    contact_info = models.TextField(max_length=500, null=True, blank=True)
    terms_and_conditions = models.TextField(max_length=500, null=True)
    company_vat = models.IntegerField(null=True)
    pan_number = models.CharField(
        max_length=200, null=False, blank=True, help_text="Enter company PAN number"
    )

    def __str__(self) -> str:
        return f"{self.company_name}"


class Config(BaseModel):
    IID_PREFIX_KEY = WEBSITE_IID_ADVANCE_SETTING
    name = models.CharField(
        max_length=100, null=False, blank=True, verbose_name="model name"
    )
    key = models.CharField(max_length=125, null=False, blank=True, unique=True)
    value = models.CharField(max_length=256, null=True, blank=True)
    config = models.JSONField(null=True, blank=True, default={})

    def delete(self):
        super().delete(self, force=True)

    def __str__(self) -> str:
        return f"{self.name}:{self.key}"

    class Meta:
        verbose_name = "Config"


class Department(BaseModel):
    IID_PREFIX_KEY = WEBSITE_IID_DEPARTMENT
    name = models.CharField(
        max_length=256,
        null=False,
        blank=True,
        unique=True,
        help_text="Enter your department name",
    )
    description = models.TextField(max_length=500, null=True, blank=True)
    contact_info = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Terminal(BaseModel):
    IID_PREFIX_KEY = WEBSITE_IID_TERMINAL
    name = models.CharField(
        max_length=256,
        null=False,
        blank=True,
    )
    terminal_ip = models.CharField(
        max_length=256,
        null=False,
        blank=True,
    )
    config = models.JSONField(default={}, null=True, blank=True)

    def __str__(self):
        return f"{self.name}=>{self.terminal_ip}"
