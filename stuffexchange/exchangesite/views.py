from django.http import HttpResponse
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, AddGoodForm, GalleryForm
from django.forms import formset_factory


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


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})


def add_good(request):
    if request.method == 'POST':
        good_form = AddGoodForm(request.POST)
        gallery_form_set = formset_factory(GalleryForm, extra=5)
        image_form = gallery_form_set(request.POST)
    else:
        good_form = AddGoodForm()
        gallery_form_set = formset_factory(GalleryForm, extra=5)
        image_form = gallery_form_set()

    return render(request, 'add_good.html', {'good_form': good_form,
                                             'image_form': image_form})
