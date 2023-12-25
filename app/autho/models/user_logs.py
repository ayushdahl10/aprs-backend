from django.db import models
from autho.models import UserDetail


class UserActivityLog(models.Model):
    user = models.ForeignKey("autho.UserDetail", on_delete=models.PROTECT, null=False)
    user_ip = models.CharField(max_length=250, null=False, blank=True)
    login_count = models.IntegerField(default=0, null=False)
    created_at = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.user}:{self.user_ip}"

    @classmethod
    def create_action_log(cls, *args, **kwargs):
        return cls.objects.create(**kwargs)
