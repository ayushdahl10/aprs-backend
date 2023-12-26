from django.db import models

from helpers.mixins.constant import WEBSITE_IID_STAFF
from helpers.models.base_model import BaseModel


class Staff(BaseModel):
    IID_PREFIX_KEY = WEBSITE_IID_STAFF
    user = models.OneToOneField(
        "autho.UserDetail", on_delete=models.PROTECT, null=False
    )
    staff_id = models.CharField(max_length=125, unique=True, null=False)
    joined_date = models.DateField(null=False)
    shift_start = models.TimeField()
    shift_end = models.TimeField()
    working_hours = models.DecimalField(max_digits=10, decimal_places=2)
    position = models.CharField(max_length=256, null=False, blank=True)
    department = models.ManyToManyField("website.Department")

    def __str__(self) -> str:
        return f"{self.staff_id} => {self.user.user.email}"

    class Meta:
        verbose_name = "Staff"

    def delete(self, force=True, *args, **kwargs):
        return super().delete(force, *args, **kwargs)
