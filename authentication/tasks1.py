from __future__ import absolute_import, unicode_literals
import datetime
import tempfile
import stripe

from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail , EmailMessage
from django.shortcuts import  redirect,get_object_or_404
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models import Sum

from user_dash.models import Vehicle
from parking.models import ParkingHistory
from authentication.models import Payment

from celery import  shared_task
from celery.decorators import periodic_task
from celery.schedules import crontab

from weasyprint import HTML

stripe.api_key= settings.STRIPE_SECRET_KEY

@shared_task
# @periodic_task(run_every=(crontab(minute='*/3')), name="some_task", ignore_result=True)
def send_email_task():
    user_ids = User.objects.filter(is_active=True).exclude(email='').values_list('id', flat=True)
    #print(user_id)
    for user_id in user_ids: 
        if Vehicle.objects.filter(user_id=user_id):  
            vehicle_ids = Vehicle.objects.filter(user_id=user_id).values_list('id', flat=True)
            # print(vehicle_id)
            for vehicle_id in vehicle_ids:
                today = datetime.datetime.today()
                last_monday = today - datetime.timedelta(days=today.weekday())
                if ParkingHistory.objects.filter(vehicle_id = vehicle_id, out_datetime__range = [last_monday,today]):  
                    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
                    history = ParkingHistory.objects.filter(vehicle_id = vehicle_id,out_datetime__range = [last_monday,today] ) 
                    user = get_object_or_404(User, pk=user_id)                                     
                    res = export_pdf(history,vehicle,user)                    
                    send_email(user,res)    
    return str('Task Complete')

def export_pdf(history,vehicle,user):
    response = HttpResponse(content_type='application/pdf')
    total = history.aggregate(Sum('charges'))
    user_id = user.id
    print(user_id)
    print(history.vehicle_id)
    print(total)
    charge_amount(user_id,total)
    html_string=render_to_string('user_dash/pdf_output.html',{'history': history,'vehicle': vehicle,'total':total['charges__sum']})
    html= HTML(string=html_string)
    result=html.write_pdf()
    return result

def charge_amount(user_id,total):
    if Payment.objects.filter(user_id= user_id):
        payment = get_object_or_404(Payment,user_id= user_id)
        print(payment.customer_id)
        charge = stripe.Charge.create(
            amount= int(total['charges__sum']*100),
            currency='inr',
            description='Payment Gateway',
            customer= payment.customer_id,
        )    
    return None 

def send_email(user,result):
    email=user.email 
    subject = 'Parking_app : Parking & Dedcuted amount deatils.'
    message = "welcome"
    email_from = settings.EMAIL_HOST_USER
    to= email
    mail = EmailMessage(
        subject,
        message,
        email_from,
        [to]
    ) 
    mail.attach('ParkingHistory.pdf', result, 'application/pdf') 
    mail.send()  
    return None

