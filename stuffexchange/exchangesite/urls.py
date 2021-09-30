from os import name
from django.urls import path

from .views import show_goods, show_good, show_user, create_exchange,\
    show_offers, user_login, register


app_name = "exchangesite"

urlpatterns = [
    path('', show_goods, name='index'),
    path('user/<int:id>', show_user, name='user'),
    path('good/<int:id>', show_good, name='good'),
    path('offers/', show_offers, name='offers'),
    path('exchange/', create_exchange, name='exchange'),
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
]