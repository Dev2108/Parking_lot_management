from django.db import models

from django.contrib.auth import models as auth_models
# Create your models here.

class Vehicle(models.Model):
    number = models.CharField(max_length=128)
    type = models.IntegerField()
    user = models.ForeignKey(auth_models.User, on_delete = models.CASCADE)
