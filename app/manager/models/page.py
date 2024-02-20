from django.db import models
from helpers.models.base_model import BaseModel
from helpers.mixins.constant import WEBSITE_IID_TEMPLATE
from manager.choices import LayoutTypes


class Page(BaseModel):
    IID_PREFIX_KEY = WEBSITE_IID_TEMPLATE
    name = models.CharField(
        max_length=256,
        blank=False,
        null=False,
        unique=True,
        help_text=("Enter the name of this page"),
    )
    page_route = models.CharField(
        max_length=256,
        null=False,
        blank=True,
        unique=True,
        help_text=("Enter the route of this page"),
    )
    component_section = models.ManyToManyField(
        "manager.ComponentSection", related_name="comp_sec"
    )
    layout_type = models.CharField(
        choices=LayoutTypes.choices,
        default=LayoutTypes.DEFAULT_LAYOUT,
        null=False,
        blank=False,
        help_text=("Choose layout for this page"),
    )
    is_authenticated = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name}"
