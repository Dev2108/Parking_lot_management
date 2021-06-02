from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


app_name = 'operators'
urlpatterns = [
    path('verify/', views.VerifyView.as_view(), name='verify'),
    path('exitscanner/', views.exitscanner, name = 'exit_scanner'),
    path('entryscanner/', views.entryscanner, name = 'entry_scanner'),
    path('entry/', views.EntryCreateAPIView.as_view(),name = 'entry'),
    path('exitupdate/', views.ExitUpdateAPIView.as_view(), name = 'exitupdate'),

]
