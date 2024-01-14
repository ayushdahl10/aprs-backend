from django.db import models

from helpers.models.base_model import BaseModel


class Message(BaseModel):
    user = models.ForeignKey("autho.UserDetail", on_delete=models.CASCADE)
    message_body = models.TextField(max_length=500, null=False, blank=True)

    def __str__(self):
        return f"{self.user.user.email}=>{self.created_at}"


class MessageRecipient(models.Model):
    message = models.ForeignKey("chat.Message", on_delete=models.PROTECT)
    is_read = models.BooleanField(default=False)
