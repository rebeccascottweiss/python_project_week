from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('dashboard',views.dashboard),
    path('<tab_id>/close_out', views.close_out),
]