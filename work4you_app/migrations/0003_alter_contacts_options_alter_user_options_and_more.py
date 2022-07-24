# Generated by Django 4.0.4 on 2022-07-21 18:42

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('work4you_app', '0002_remove_candidate_user_remove_employer_user_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contacts',
            options={'ordering': ['id', 'email', 'phone1', 'phone2'], 'verbose_name': 'Контакти компанії', 'verbose_name_plural': 'Контакти компанії'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['id', 'first_name', 'last_name'], 'verbose_name': 'Користувачі', 'verbose_name_plural': 'Користувачі'},
        ),
        migrations.AlterField(
            model_name='candidate',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 21, 21, 42, 33, 866089), verbose_name='Дата реєстрації'),
        ),
        migrations.AlterField(
            model_name='employer',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='work4you_app.company', verbose_name='Компанія'),
        ),
        migrations.AlterField(
            model_name='employer',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 21, 21, 42, 33, 867089), verbose_name='Дата реєстрації'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 21, 21, 42, 33, 863090), verbose_name='Дата додавання'),
        ),
    ]
