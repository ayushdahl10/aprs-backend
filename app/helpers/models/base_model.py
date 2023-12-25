from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from helpers.mixins.helper import GenerateIID


# Create your models here.
class BaseModel(models.Model):
    IID_PREFIX_KEY = ""
    iid = models.CharField(max_length=256, null=False, blank=True, editable=False)
    created_at = models.DateTimeField(null=False, blank=True)
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        related_name="%(class)s_created_by",
    )
    updated_by = models.CharField(max_length=256, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False, editable=False)

    class Meta:
        abstract = True

    def delete(self, force=False, *args, **kwargs):
        if force:
            return super().delete(*args, **kwargs)
        self.is_deleted = True
        self.is_active = False
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.iid:
            self.iid = GenerateIID.generate_iid(self, self.IID_PREFIX_KEY)
        if not self.created_at:
            self.created_at = datetime.now()
        super().save(*args, **kwargs)
