from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'user'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('add/', views.addvehicle, name='add_vehicle'),
    path('vehicles/', views.listvehicles, name = 'view_vehicles' ),
    path('<int:vehicle_id>/qrcode/', views.return_qr, name = 'return_qr'),
    path('history/', views.vehicleparking, name = 'history'),
    path('<int:vehicle_id>/vehicles_history/', views.parking_history, name = 'vehicles_history'),

]
