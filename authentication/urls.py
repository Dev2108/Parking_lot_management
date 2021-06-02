from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from . import views

app_name = 'auth'
urlpatterns = [
     path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('signup/',views.signup, name = 'signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('credit_card/',views.CreditPageView.as_view(), name = 'credit_card'),
    path('charge/',views.charge, name ='charge'),
    path('zoom_callback/', views.Zoom_callback, name='Zoom_callback'),
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',views.activate, name='activate'),
    # url(r'^google-login/$', views.google_login, name="google_login"),
   
]




 #url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
