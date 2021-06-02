import datetime
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User

from user_dash.models import Vehicle
from .models import ParkingHistory

# Create your views here.
def entry(request, vehicle_id):
    user = request.user
    vehicle = get_object_or_404(Vehicle, pk = vehicle_id)
    if ParkingHistory.objects.get(vehicle_id = vehicle_id, out_datetime = None):
        return redirect('/operators/qr_scanner/')

    entry_object = ParkingHistory(vehicle = vehicle)
    entry_object.save()
    return redirect('/user/vehicles/')

def exit(request, vehicle_id):
    user = request.user
    vehicle = get_object_or_404(Vehicle, pk = vehicle_id)
    try:
        exit_updation = ParkingHistory.objects.get(vehicle_id = vehicle_id, out_datetime = None)
        exit_updation.out_datetime = timezone.now()
        exit_updation.charges =round(charge(exit_updation.in_datetime, exit_updation.out_datetime),2)
        exit_updation.save()
    except ObjectDoesNotExist:
        print("ObjectDoesNotExist")
    return redirect('/user/')


def charge(in_time, out_time):
    datetimeFormat = '%Y-%m-%d %H:%M:%S'
    diff = out_time - in_time
    return diff.seconds/60*0.25

    # days = * 3600 * 24
    # hours =  * 3600
    # minutes =  * 60
