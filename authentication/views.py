import stripe
import requests
import datetime
import json
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, views
from django.views import generic
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.urls import reverse
from django.http import HttpResponse

from .tokens import account_activation_token
from .forms import SignUpForm
from django.conf import settings
from django.core.mail import send_mail
from .models import Payment
from .tasks1 import send_email_task

from django.core.mail import EmailMessage
from authentication.models import Payment
import threading
from weasyprint import HTML
stripe.api_key= settings.STRIPE_SECRET_KEY


class EmailThread(threading.Thread):
    def __init__(self, email):  
        self.email=email
        threading.Thread.__init__(self)
    
    def run(self):
        self.email.send()

def home(request):
    return render(request, 'authentication/home.html')

class CreditPageView(TemplateView):
    template_name = "authentication/credit_card.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['key']=settings.STRIPE_PUBLISHABLE_KEY
        
        return context

def charge(request):
    if request.method=='POST':
        customer=stripe.Customer.create( 
            email=request.user.email,
            source=request.POST['stripeToken'],
        )
        
        
        charge = stripe.Charge.create(
            amount=2000,
            currency='inr',
            description='Payment Gateway',
            customer= customer.id,
        ) 
        user=request.user

        payment=Payment( user= user, status=True, customer_id=customer.id)
        payment.save()        
        return redirect('/user/')


def account_activation_sent(request):
    return render(request, 'authentication/account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)

        return redirect('/auth/credit_card/')
    else:
        return render(request, 'account_activation_invalid.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create(username=form.cleaned_data.get('email'))
            raw_password=user.set_password(raw_password=form.cleaned_data.get('password1', None))
            user.is_active = False
            user.email=form.cleaned_data.get('email')
            user.save()

            # email = user.email
            # send_email(email)
            current_site = get_current_site(request)
            subject = 'Parking App  : Account Activated Successfully.'
            message = render_to_string('authentication/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email_from = settings.EMAIL_HOST_USER
            to=user.email
            email= EmailMessage(
                subject,
                message,
                email_from,
                [to]
            ) 
            EmailThread(email).start()            
            return redirect('/auth/account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'authentication/signup.html', {'form': form})


# def base64_encode(message):
#     import base64
#     message_bytes = message.encode('ascii')
#     base64_bytes = base64.b64encode(message_bytes)
#     base64_message = base64_bytes.decode('ascii')name 'header' is not defined
#     return base64_message



def Zoom_callback(request):
    code = request.GET["code"]
    print(code)
    response = requests.post(f"https://zoom.us/oauth/token?grant_type=authorization_code&code={code}&redirect_uri=http://127.0.0.1:8000/auth/zoom_callback/" ,  headers = {
       "Authorization": "Basic VWVEa0RDMnJTY1NtdjZWdnNya2lOdzpuTkM4djJpRzA1RUU1WU9ITzllTHJHSGtOVzJwMXBQcQ=="
    })

    # zoom_access_token = response.json().get("access_token")
    
    response = requests.post("https://api.zoom.us/v2/users/me/meetings", headers={
        'Content-Type': "application/json",
        "Authorization": f"Bearer {response.json().get('access_token')}"
    },data=json.dumps({
            "topic": "Interview with PRASHANT",
            "type": 2,
            "start_time": str(datetime.datetime.utcnow()),
            "password" : settings.ZOOM_PASS,
        })) 
    
    return render(request, 'authentication/zoom.html', {'join':response.json()["join_url"], 'start': response.json()["start_url"], 'start_time' : response.json()['start_time']})
    
    
    
    
    
    
    
    
    
    
    # else:
    #     return HttpResponseRedirect("/auth/")

# def send_email(email):
    
#     print(email)
#     send_email_task.delay(email)
# def google_login(request):
#     redirect_uri = "%s://%s%s" % (
#         request.scheme, request.get_host(), reverse('auth:google_login')
#     )
#     if('code' in request.GET):
#         params = {
#             'grant_type': 'authorization_code',
#             'code': request.GET.get('code'),
#             'redirect_uri': redirect_uri,
#             'client_id': settings.GP_CLIENT_ID,
#             'client_secret': settings.GP_CLIENT_SECRET
#         }
#         token_url = 'https://accounts.google.com/o/oauth2/token'
#         response = requests.post(token_url, data=params)
#         url = 'https://www.googleapis.com/oauth2/v1/userinfo'
#         access_token = response.json().get('access_token')
#         response = requests.get(url, params={'access_token': access_token})
#         user_data = response.json()
#         email = user_data.get('email')
#         if email:
#             user, _ = User.objects.get_or_create(email=email, username=email)
            
#             data = {
#                 'first_name': user_data.get('name', '').split()[0],
#                 'last_name': user_data.get('family_name'),
#                 'google_avatar': user_data.get('picture'),
#                 'is_active': False
#             }
#             user.__dict__.update(data)
#             user.save()
#             user.backend = settings.AUTHENTICATION_BACKENDS[0]
#             login(request, user)
            
#             current_site = get_current_site(request)
#             subject = 'Parking App  : Account Activated Successfully.'
#             message = render_to_string('authentication/account_activation_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': account_activation_token.make_token(user),
#             })
#             email_from = settings.EMAIL_HOST_USER
#             to=user.email
#             email= EmailMessage(
#                 subject,
#                 message,
#                 email_from,
#                 [to]
#             ) 
#             EmailThread(email).start() 
#             return redirect('/auth/account_activation_sent')           
#         else:
#             messages.error(
#                 request,
#                 'Unable to login with Gmail Please try again'
#             )
#         return render(request, 'authentication/signup.html', {'form': form})

#     else:
#         url = "https://accounts.google.com/o/oauth2/auth?client_id=%s&response_type=code&scope=%s&redirect_uri=%s&state=google"
#         scope = [
#             "https://www.googleapis.com/auth/userinfo.profile",
#             "https://www.googleapis.com/auth/userinfo.email"
#         ]
#         scope = " ".join(scope)
#         url = url % (settings.GP_CLIENT_ID, scope, redirect_uri)
#         return redirect(url)