from django.urls import path
from . import views

urlpatterns = [
    path('',  views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('send-otp/', views.SendOTPView.as_view(), name='send_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('about/', views.about, name='about'),
    path('contactus/', views.contactus, name='contactus'),
    path('tnc/', views.tnc, name='tnc'),
    path('guidelines/', views.guidelines, name='guidelines'),
    path('faq/', views.faq, name='faq'),
]
