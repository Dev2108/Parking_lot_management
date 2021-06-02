from django import forms

vehicle_type= [
    (2, '2 Wheeler'),
    (4, '4 Wheeler'),
    ]
class AddVehicle(forms.Form):

    number = forms.CharField(label='Vehicle Number',max_length=128)
    type= forms.IntegerField(label='Vehicle Type', widget=forms.Select(choices=vehicle_type))
