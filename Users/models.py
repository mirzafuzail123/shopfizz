from pickle import TRUE
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
   is_customer=models.BooleanField(default=True)
   is_seller=models.BooleanField(default=False)
   as_seller=models.BooleanField(default=False)