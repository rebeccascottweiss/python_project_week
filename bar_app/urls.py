from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('managerdash/addemployee/register', views.register),
    path('login', views.login),
    path('dashboard',views.dashboard),
    path('dashboard/managerdash', views.managerdash),
    path('<tab_id>/close_out', views.close_out),
    path('addemployee', views.addemployee),
    path('adddrink', views.adddrink),
    path('adddrink/new', views.newdrink),
    path('drinks', views.drinks)
]
