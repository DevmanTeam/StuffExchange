from django.urls import path
from django.views.generic import TemplateView
from . import views


app_name = "exchangesite"

urlpatterns = [
    path('', views.show_goods, name='index'),
    path('user/<int:user_id>', views.show_user, name='user'),
    path('good/<int:good_id>', views.show_good, name='good'),
    path('good/<int:good_id>/update/', views.update_good, name='update_good'),
    path('good/<int:good_id>/delete/good_id', views.delete_good, name='delete_good'),
    path('offers/', views.show_offers, name='offers'),
    path('exchange/<int:user_id>-<int:good_id>',
        views.create_exchange,
         name='exchange'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('add_good/', views.add_good, name='add_good'),
    path('add_good_done/', views.add_good_done, name='add_good_done'),
    path('already_exist/', TemplateView.as_view(template_name="already_exist.html"), name='already_exist'),

]
