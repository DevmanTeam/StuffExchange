from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    communication_contact = models.CharField('контакт для связи', max_length=100)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Good(models.Model):

    CATEGORY_CHOICES = [
        ("Транспорт", "транспорт"),
        ("Одежда, обувь", "одежда, обувь"),
        ("Детская одежда и обувь", "детская одежда и обувь"),
        ("Игрушки и детские вещи", "игрушки и детские вещи"),
        ("Бытовая техника", "бытовая техника"),
        ("Мебель и интерьерные вещи", "мебель и интерьерные вещи"),
        ("Кухонная утварь", "кухонная утварь"),
        ("Продукты питания", "продукты питания"),
        ("Вещи для ремонта и строительства", "вещи для ремонта и строительства"),
        ("Растения", "растения"),
        ("Электроника", "электроника"),
        ("Спортивные вещи", "спортивные вещи"),
        ("Вещи для творчества и хобби", "вещи для творчества и хобби"),
        ("Коллекционные вещи", "коллекционные вещи"),
    ]

    category = models.CharField('название категории',
                                max_length=50,
                                choices=CATEGORY_CHOICES,
                                db_index=True)
    title = models.CharField('название вещи', max_length=100)
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             related_name='goods',
                             verbose_name="Пользователь")

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.title


class Gallery(models.Model):

    image = models.ImageField('фото товара', null=True, blank=True)
    good = models.ForeignKey(Good,
                             on_delete=models.CASCADE,
                             related_name='images',
                             verbose_name="Товар")

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        return f'Фото товара {self.good.title}'


class ExchangeFromUserToUser(models.Model):

    good = models.ForeignKey(Good,
                             on_delete=models.CASCADE,
                             related_name='exchange_good',
                             verbose_name="Товар для обмена")
    from_user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             related_name='exchange_from',
                             verbose_name='Кто предлагает обмен')
    to_user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             related_name='exchange_to',
                             verbose_name="Кому предлагают обмен")

    class Meta:
        verbose_name = 'Товар для обмена'
        verbose_name_plural = 'Товары для обмена'

    def __str__(self):
        return self.good.title