import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User , Group
from django.utils import timezone
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status

from parking import views
from parking.views import charge
from user_dash.models import Vehicle
from parking.models import ParkingHistory
from .forms import QRForm
from .serializers import EntrySerializer
from .mixins import CSRFExemptMixin
from .custom_authentication_classes import CsrfExemptSessionAuthentication

# Create your views here.

class VerifyView(View):
    
    def get(self,request):

        try:
            enter=request.user
            user=User.objects.get(id=enter.id)
            group=Group.objects.get(id=1)
            group_1=user.groups.get(id=group.id)
        except:
            return redirect('/user/')
        return render(request, 'operator/op_dashboard.html')

def entryscanner(request):
    
    return render(request, 'operator/entry_operator.html')

def exitscanner(request):
    return render(request, 'operator/exit_operator.html')

class EntryCreateAPIView(CreateAPIView):

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = EntrySerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vehicle = get_object_or_404(Vehicle, number = serializer.data.get('number'), user_id = serializer.data.get('user_id'))

        if ParkingHistory.objects.filter(vehicle_id = vehicle.id, out_datetime = None).exists():
            return Response(
                data={
                    'detail': 'The Vehicle is inside the parking lot'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        entry_object = ParkingHistory(vehicle = vehicle)
        entry_object.save()
        return Response(
            data={
            'detail': 'Entry Successful'
            },
            status=status.HTTP_200_OK
        )

class ExitUpdateAPIView(UpdateAPIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = EntrySerializer
    model = ParkingHistory
    queryset= ParkingHistory.objects.all()

    def update(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            vehicle = get_object_or_404(Vehicle, number = serializer.data.get('number'), user_id = serializer.data.get('user_id'))
            instance = ParkingHistory.objects.get(vehicle_id = vehicle.id, out_datetime = None)
            instance.out_datetime = timezone.now()
            instance.charges = round(charge(instance.in_datetime, instance.out_datetime),2)
            instance.save()
        except ObjectDoesNotExist:
            return Response(
                data={
                    'detail': 'Vehicle has no entry'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            data={
            'detail': 'Exit Successful'
            },
            status=status.HTTP_200_OK
        )

