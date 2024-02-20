from django.db import models
from helpers.models.base_model import BaseModel
from helpers.mixins.constant import WEBSITE_IID_TEMPLATE_MANAGER


# Create your models here.
class TemplateManager(BaseModel):
    IID_PREFIX_KEY = WEBSITE_IID_TEMPLATE_MANAGER
    name = models.CharField(max_length=256, null=False, blank=False, unique=True)
    icon = models.ImageField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"
