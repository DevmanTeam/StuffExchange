from django.http import HttpResponse
from django.contrib.auth import views as auth_views


def show_goods(request):
    return HttpResponse('<h1>Это главная страница!</h1>')


def show_good(request):
    return HttpResponse('<h1>Это страница вещи!</h1>')


def show_user(request):
    return HttpResponse('<h1>Это страница юзера с товарами!</h1>')


def create_exchange(request):
    return HttpResponse('<h1>Здесь создаём предложение для обмена вещи!</h1>')


def show_offers(request):
    return HttpResponse('<h1>Здесь показываем какие у нас есть предложения по обмену вещей!</h1>')
