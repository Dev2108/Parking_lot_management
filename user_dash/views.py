from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views import generic
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.encoding import force_text,force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import base64
from .decorators import payment_req
from .qr_generator import generation
from .forms import AddVehicle
from .models import Vehicle
from parking.models import ParkingHistory

# Create your views here.
@login_required
def index(request):
    login_url = '/login/'
    return render(request,'user_dash/index.html')

@payment_req()
@login_required
def addvehicle(request):
    login_url = '/login/'
    if request.method == 'POST':
        form = AddVehicle(request.POST)
        if form.is_valid():
            user = request.user
            veh_number = form.cleaned_data.get('number')
            veh_type = form.cleaned_data.get('type')
            if Vehicle.objects.filter(number = veh_number):
                return redirect('/user/')
            vehicle_object=Vehicle(number = veh_number, type = veh_type, user = user )
            vehicle_object.save()
            return redirect('/user/vehicles/')
    else:
        form = AddVehicle()
    return render(request, 'user_dash/add_vehicle.html', {'form': form})

@login_required
def listvehicles(request):
    login_url = '/login/'
    user = request.user
    vehicles = Vehicle.objects.filter(user_id = user.id )

    return render(request,'user_dash/vehicles.html', {"list":vehicles})

@login_required
def return_qr(request, vehicle_id):
    login_url = '/login/'
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    data = vehicle.number+','+str(vehicle.user.id)
    qr = generation(data)
    img_name = 'media/images/'+str(request.user.id)+str(vehicle.number)+'.png'
    qr.save(img_name)
    hosted_link = 'http://127.0.0.1:8000/'+img_name
    return render(request, 'user_dash/vehicle_qr.html',{'image': hosted_link})

@login_required
def vehicleparking(request):
    login_url = '/login/'
    user = request.user
    vehicles = Vehicle.objects.filter(user_id = user.id )
    return render(request,'user_dash/user_history.html', {"list":vehicles})


@login_required
def parking_history(request, vehicle_id):
    login_url = '/login/'
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    history = ParkingHistory.objects.filter(vehicle = vehicle)
    return render(request,'user_dash/history.html', {"history":history, "vehicle":vehicle})
