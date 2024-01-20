from django.db import models

from helpers.models.base_model import BaseModel


class Type(models.TextChoices):
    GET = ("get"), ("GET")
    POST = ("post"), ("POST")
    PUT = ("put"), ("PUT")
    DELETE = ("delete"), ("DELETE")
    PATCH = ("patch"), ("PATCH")


# Create your models here.


class Permission(models.Model):
    url_name = models.CharField(max_length=256)
    url_type = models.CharField(choices=Type.choices, max_length=25)

    def __str__(self):
        return f"{self.url_name}:{self.url_type}"


class Role(models.Model):
    name = models.CharField(max_length=125, null=False, blank=True, unique=True)
    description = models.TextField(max_length=300, null=True)
    permissions = models.ManyToManyField(Permission, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"
