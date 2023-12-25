from django.db import models
from helpers.models.base_model import BaseModel


class Staff(BaseModel):
    user = models.OneToOneField(
        "autho.UserDetail", on_delete=models.PROTECT, null=False
    )
    staff_id = models.CharField(max_length=125, unique=True, null=False)
    joined_date = models.DateField(null=False)
    shift_start = models.TimeField()
    shift_end = models.TimeField()
    working_hours = models.DecimalField(max_digits=10, decimal_places=2)
    position = models.CharField(max_length=256, null=False, blank=True)

    def __str__(self) -> str:
        return f"{self.staff_id} => {self.user.user.email}"

    class Meta:
        verbose_name = "Staff"

    def delete(self, force=True, *args, **kwargs):
        return super().delete(force, *args, **kwargs)
