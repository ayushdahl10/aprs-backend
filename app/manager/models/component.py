from django.db import models
from helpers.models.base_model import BaseModel
from helpers.mixins.constant import (
    WEBSITE_IID_COMPONENT,
    WEBSITE_IID_SECTION,
    WEBSITE_IID_COMPONENT_SECTION,
)
from manager.choices import SectionTypes


# Create your models here.
class Component(BaseModel):
    IID_PREFIX_KEY = WEBSITE_IID_COMPONENT
    name = models.CharField(max_length=256, blank=False, null=False, unique=True)
    path = models.CharField(
        max_length=500, blank=False, null=False, help_text="File path to your component"
    )

    def __str__(self) -> str:
        return f"{self.name}"


class Section(BaseModel):
    IID_PREFIX_KEY = WEBSITE_IID_SECTION
    name = models.CharField(
        choices=SectionTypes.choices,
        default=SectionTypes.HEADER,
        blank=False,
        null=False,
    )

    def __str__(self) -> str:
        return f"{self.name}"


class ComponentSection(BaseModel):
    IID_PREFIX_KEY = WEBSITE_IID_COMPONENT_SECTION
    section = models.ForeignKey("manager.Section", on_delete=models.PROTECT, null=False)
    component = models.ForeignKey(
        "manager.Component", on_delete=models.PROTECT, null=False
    )
    order = models.IntegerField(null=False, blank=False)

    def __str__(self) -> str:
        return f"{self.section.name}:{self.component.name}"

    class Meta:
        unique_together = ("section", "component")

    def delete(self, force=True, *args, **kwargs):
        return super().delete(force, *args, **kwargs)
