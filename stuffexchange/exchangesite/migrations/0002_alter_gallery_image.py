# Generated by Django 3.2.7 on 2021-09-30 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchangesite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='фото товара'),
        ),
    ]
