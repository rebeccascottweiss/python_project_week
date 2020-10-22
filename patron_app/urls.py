from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('register', views.register),
    path('login', views.login),
    path('start_tab', views.start_tab),
    path('add_payment', views.add_payment),
    path('patron_tab', views.patron_tab),
    path('pay_tab', views.pay_tab),
    path('tab_receipt', views.tab_receipt),
    path('patron/account', views.account),
    path('patron/update_info', views.update_info),
    path('patron/password_update', views.password_update),
    path('patron/password_change', views.password_change),
    path('tip_select', views.tip_select),
    path('return_home', views.return_home),
    path('logout', views.logout),
    path('card_wallet', views.card_wallet),
]