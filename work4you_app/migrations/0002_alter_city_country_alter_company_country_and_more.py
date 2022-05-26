# Generated by Django 4.0.4 on 2022-05-25 15:27

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('work4you_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='country',
            field=models.ForeignKey(default='Україна', on_delete=django.db.models.deletion.CASCADE, to='work4you_app.country'),
        ),
        migrations.AlterField(
            model_name='company',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='work4you_app.country', verbose_name='Країна'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 25, 18, 27, 50, 339481), verbose_name='Дата додавання'),
        ),
    ]
