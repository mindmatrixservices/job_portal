from django.urls import path
from . import views

urlpatterns = [
    path('',  views.home, name='home'),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('contactus/', views.contactus, name='contactus'),
    path('tnc/', views.tnc, name='tnc'),
    path('guidelines/', views.guidelines, name='guidelines'),
    path('faq/', views.faq, name='faq'),
]
