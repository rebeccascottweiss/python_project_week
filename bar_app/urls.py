from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('addemployee/register', views.register),
    path('login', views.login),
    path('cashout', views.cashout),
    path('dashboard',views.dashboard),
    path('drinks/delete/<number>', views.deletedrink)
    path('dashboard/managerdash', views.managerdash),
    path('addemployee', views.addemployee),
    path('adddrink', views.adddrink),
    path('adddrink/new', views.newdrink),
    path('drinks', views.drinks), 
    path('adddrink/<tab_id>', views.add_order),
    path('delete_drink/<tab_id>/<drink_id>', views.delete_drink),
    path('close_out/<tab_id>', views.close_out),
    path('edit/<tab_id>', views.edit_tab),
]
