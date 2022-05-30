# Generated by Django 4.0.4 on 2022-05-27 21:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work4you_app', '0016_remove_vacancy_salary_type_vacancy_employment_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 28, 0, 25, 59, 917433), verbose_name='Дата додавання'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='employment_type',
            field=models.CharField(choices=[('Повна зайнятість', 'Повна зайнятість'), ('Неповна зайнятість', 'Неповна зайнятість'), ('Дистанційна робота', 'Дистанційна робота')], default='Повна зайнятість', max_length=100, verbose_name='Тип зайнятості'),
        ),
    ]
