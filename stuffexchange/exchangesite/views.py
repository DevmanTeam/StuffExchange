from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm, AddGoodForm, GalleryForm
from django.forms import formset_factory
from django.contrib.auth.views import LoginView

from .models import Good, ExchangeFromUserToUser, CustomUser, Gallery


def show_goods(request):
    goods = Good.objects.exclude(user__id=request.user.id)
    goods_to_image = {}
    for good in goods:
        image_url = good.images.first().image.url
        goods_to_image[good] = image_url
    return render(request, 'goods.html', {'goods_to_image': goods_to_image})


def show_good(request, good_id):
    good = Good.objects.filter(id=good_id).first()
    images = Gallery.objects.filter(good=good)
    return render(request, 'good.html', {'good': good, 'images': images})


def show_user(request, user_id):
    user = CustomUser.objects.filter(id=user_id).first()
    goods = Good.objects.filter(user=user)
    return render(request, 'user_goods.html', {'goods': goods, 'user': user})


def create_exchange(request, user_id, good_id): # Юра
    from_user = CustomUser.objects.filter(id=request.user.id).first()
    to_user = CustomUser.objects.filter(id=user_id).first()
    good = Good.objects.filter(id=good_id).first()
    exchange, created = ExchangeFromUserToUser.objects.get_or_create(from_user=from_user, to_user=to_user, good=good)
    print(exchange, created)
    return redirect('exchangesite:offers')


def show_offers(request): # Юра
    offers = ExchangeFromUserToUser.objects.filter(to_user=request.user)
    return render(request, 'offers.html', {'offers': offers})


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


def update_good(request, good_id):

    if request.method == 'GET':

        good = Good.objects.get(id=good_id)
        good_form = AddGoodForm(instance=good)
        images_form = []
        for image in good.images.all():
            image_form = GalleryForm(instance=image)
            images_form.append(image_form)
        while len(images_form) < 5:
            images_form.append(GalleryForm())
        # gallery_form_set = formset_factory(GalleryForm, extra=5)
        # image_form = gallery_form_set()
        return render(request, 'update_good.html', {'good_form': good_form,
                                                    'images_form': images_form})
    else:
        good = Good.objects.get(id=good_id)
        good_form = AddGoodForm(request.POST, instance=good)
        gallery_form_set = formset_factory(GalleryForm, extra=5)
        image_formset = gallery_form_set(request.POST, request.FILES)
        if good_form.is_valid() :
            new_good = good_form.save()
            return redirect('exchangesite:good', good_id=good_id)


def add_good(request):

    if request.method == 'POST':
        good_form = AddGoodForm(request.POST)
        gallery_form_set = formset_factory(GalleryForm, extra=5)
        image_formset = gallery_form_set(request.POST, request.FILES)
        if good_form.is_valid() and image_formset.is_valid():
            cd_good = good_form.cleaned_data
            new_good = Good.objects.create(category=cd_good['category'],
                                    title=cd_good['title'],
                                    description=cd_good['description'],
                                    user=request.user)
            cd_images = image_formset.cleaned_data
            for cd_image in cd_images:
                if cd_image:
                    Gallery.objects.create(image=cd_image['image'],
                                           good=new_good)
        return redirect('exchangesite:user', user_id=request.user.id)
    else:
        good_form = AddGoodForm()
        gallery_form_set = formset_factory(GalleryForm, extra=5)
        image_formset = gallery_form_set()

    return render(request, 'add_good.html', {'good_form': good_form,
                                             'image_formset': image_formset})
