from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'parking'

urlpatterns = [
    path('<int:vehicle_id>/entry/', views.entry, name = 'entry'),
    path('<int:vehicle_id>/exit/', views.exit, name = 'exit'),

]
