from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('bar/register', views.register),
    path('bar/login', views.login),
    path('bar/dashboard', views.dashboard),
]