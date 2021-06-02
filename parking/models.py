from django.db import models

from user_dash.models import Vehicle
# Create your models here.
class ParkingHistory(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete = models.CASCADE)
    
    in_datetime = models.DateTimeField(auto_now_add = True)
    out_datetime = models.DateTimeField(null = True)
    charges = models.FloatField(null = True)
    