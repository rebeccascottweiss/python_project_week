from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('register', views.register),
    path('login', views.login),
    path('start_tab', views.start_tab),
    path('add_payment', views.add_payment),
    path('patron_tab', views.patron_tab),
    # path('pay_tab', views.pay_tab),
    path('logout', views.logout),
]