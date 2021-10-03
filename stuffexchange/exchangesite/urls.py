from django.urls import path

from .views import show_goods, show_good, show_user, create_exchange, \
    show_offers, user_login, register, add_good, logout_view, update_good, \
    add_good_done, delete_good

app_name = "exchangesite"

urlpatterns = [
    path('', show_goods, name='index'),
    path('user/<int:user_id>', show_user, name='user'),
    path('good/<int:good_id>', show_good, name='good'),
    path('good/<int:good_id>/update/', update_good, name='update_good'),
    path('good/<int:good_id>/delete/good_id', delete_good, name='delete_good'),
    path('offers/', show_offers, name='offers'),
    path('exchange/<int:user_id>-<int:good_id>',
         create_exchange,
         name='exchange'),
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('add_good/', add_good, name='add_good'),
    path('add_good_done/', add_good_done, name='add_good_done'),
]
