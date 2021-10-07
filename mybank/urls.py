from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('account_status/', views.user_accnt, name = "account_status"),
    path('money_transfer/', views.money_transfer, name = "money_transfer"),
]
