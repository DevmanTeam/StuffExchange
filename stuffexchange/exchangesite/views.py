from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, UserRegistrationForm, GoodForm, GalleryFormSet
from .models import Good, ExchangeFromUserToUser, CustomUser, Gallery


def show_goods(request):
    if request.user.is_authenticated:
        goods = Good.objects.exclude(user__id=request.user.id)
    else:
        goods = Good.objects.all()

    return render(request, 'goods.html', {'goods': goods})


def show_good(request, good_id):
    good = Good.objects.filter(id=good_id).first()
    images = Gallery.objects.filter(good=good)
    return render(request, 'good.html', {'good': good, 'images': images})


def show_user(request, user_id):
    user = CustomUser.objects.filter(id=user_id).first()
    goods = Good.objects.filter(user=user)
    context = {
        'user_profile': user,
        'goods': goods
    }
    return render(request, 'user_goods.html', context)


@login_required
def create_exchange(request, user_id, good_id):
    if request.user.is_authenticated:
        from_user = CustomUser.objects.filter(id=request.user.id).first()
        to_user = CustomUser.objects.filter(id=user_id).first()
        good = Good.objects.filter(id=good_id).first()
        if from_user != to_user and good and from_user and to_user:
            exchange, created = ExchangeFromUserToUser.objects.get_or_create(from_user=from_user, to_user=to_user, good=good)
            print(exchange, created)
            return redirect('exchangesite:already_exist')
            
    return redirect('exchangesite:offers')


@login_required
def show_offers(request):
    offers_to_user = ExchangeFromUserToUser.objects.filter(to_user=request.user)
    offers_from_user = ExchangeFromUserToUser.objects.filter(from_user=request.user)
    return render(request, 'offers.html', {'offers_to_user': offers_to_user, 'offers_from_user': offers_from_user},)


def logout_view(request):
    logout(request)
    return redirect('exchangesite:index')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('exchangesite:index')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login or password')
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


@login_required
def add_good(request):
    if request.method == 'POST':
        good_form = GoodForm(request.POST)
        if good_form.is_valid():
            cd_good = good_form.cleaned_data
            good = Good.objects.create(category=cd_good['category'],
                                    title=cd_good['title'],
                                    description=cd_good['description'],
                                    user=request.user)
            image_formset = GalleryFormSet(request.POST, request.FILES, instance=good)
            if image_formset.is_valid():
                image_formset.save()
        return redirect('exchangesite:add_good_done')
    else:
        good_form = GoodForm()
        image_formset = GalleryFormSet()

    return render(request, 'add_good.html', {'good_form': good_form,
                                             'image_formset': image_formset,})


@login_required
def update_good(request, good_id):
    good = Good.objects.get(id=good_id)
    if request.method == 'GET':
        good_form = GoodForm(instance=good)
        image_formset = GalleryFormSet(instance=good)
        return render(request, 'update_good.html', {'good_form': good_form,
                                                    'image_formset': image_formset})
    else:
        good_form = GoodForm(request.POST, instance=good)
        if good_form.is_valid():
            good.save()
            image_formset = GalleryFormSet(request.POST, request.FILES,
                                           instance=good)
            if image_formset.is_valid():
                image_formset.save()
            return redirect('exchangesite:update_good_done', good_id=good_id)


@login_required
def add_good_done(request):
    return render(request, 'add_good_done.html')


@login_required
def update_good_done(request, good_id):
    return render(request, 'update_good_done.html')


@login_required
def delete_good(request, good_id):
    good = Good.objects.filter(id=good_id)
    good.delete()
    return render(request, 'delete_good.html')
