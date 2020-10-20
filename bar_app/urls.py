from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('addemployee/register', views.register),
    path('login', views.login),
    path('cashout', views.cashout),
    path('dashboard',views.dashboard),
    path('<tab_id>/close_out', views.close_out),
    path('drinks/delete/<number>', views.deletedrink),
    path('addemployee', views.addemployee),
    path('adddrink', views.adddrink),
    path('adddrink/new', views.newdrink),
    path('drinks', views.drinks), 
    path('switch_employee', views.switch_employee),
    path('adddrink/<tab_id>', views.add_order),
    path('delete_drink/<tab_id>/<drink_id>', views.delete_drink),
    path('close_out/<tab_id>', views.close_out),
    path('edit/<tab_id>', views.edit_tab),
]
