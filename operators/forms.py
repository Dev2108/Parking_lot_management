from django import forms
from django.contrib.auth.forms import UserCreationForm
from  parking.models import ParkingHistory


class QRForm(forms.Form):
    qrdata = forms.CharField(max_length=12, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    user = forms.IntegerField(label='User ID', widget=forms.TextInput(attrs={'readonly':'readonly'}))
