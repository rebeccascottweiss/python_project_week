from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('addemployee/register', views.register),
    path('login', views.login),
    path('dashboard',views.dashboard),
    path('<tab_id>/close_out', views.close_out),
    path('addemployee', views.addemployee),
    path('adddrink', views.adddrink),
    path('adddrink/new', views.newdrink),
    path('drinks', views.drinks),
    path('employees', views.employees),
    path('drinks/delete/<number>', views.deletedrink)
]
