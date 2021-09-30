from django.contrib import admin
from exchangesite.models import CustomUser,\
    Good,\
    Gallery,\
    ExchangeFromUserToUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass


class GalleryInline(admin.TabularInline):
    model = Gallery


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    inlines = [GalleryInline]


@admin.register(ExchangeFromUserToUser)
class ExchangeFromUserToUserAdmin(admin.ModelAdmin):
    pass


