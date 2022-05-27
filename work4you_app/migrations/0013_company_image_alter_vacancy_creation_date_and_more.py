# Generated by Django 4.0.4 on 2022-05-27 16:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work4you_app', '0012_alter_company_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/', verbose_name='Компания'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 27, 19, 37, 53, 646022), verbose_name='Дата додавання'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='currency',
            field=models.CharField(choices=[('HRYVNIA', 'HRYVNIA'), ('DOLLAR', 'DOLLAR'), ('EURO', 'EURO')], max_length=10, verbose_name='Валюта'),
        ),
    ]
