from django.db import models
from django.contrib.auth.models import User
from helpers.models.base_model import BaseModel

# Create your models here.

# class User(User):
#     username=models.CharField(max_length=256,unique=True,null=False,blank=True)
#     email=models.CharField(max_length=256,unique=True,null=False,blank=True)
#     password=models.CharField(max_length=126,null=False,blank=True)
#     first_name=models.CharField(max_length=256,null=False,blank=True)
#     last_name=models.CharField(max_length=256,null=False,blank=True)


class OrderHistory(BaseModel):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    last_order_address = models.CharField(max_length=126, null=False)
    
    
