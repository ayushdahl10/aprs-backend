from helpers.models.base_model import BaseModel
from autho.models import User
from django.db import models
from helpers.mixins.constant import WEBSITE_IID_PROPERTY


class Property(BaseModel):
    IID_PREFIX_KEY = WEBSITE_IID_PROPERTY
    company = models.ForeignKey("website.Company", on_delete=models.PROTECT, null=True)
    owner = models.ManyToManyField(User)
    name = models.CharField(max_length=256, null=False, blank=True, default="")
    description = models.TextField(max_length=1000, null=False)
    location = models.CharField(max_length=125, null=False, blank=False, default="")
    gallery = models.ImageField(upload_to="image/property/", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Properties"

    def __str__(self) -> str:
        return f"{self.name}"
