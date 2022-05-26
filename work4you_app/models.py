import datetime

from django.db import models


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name="Країна")

    class Meta:
        verbose_name = "Країни"
        verbose_name_plural = "Країни"
        ordering = ['title', 'id']

    def __str__(self):
        return self.title


class City(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name="Місто")
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE, default="Україна")

    class Meta:
        verbose_name = "Міста"
        verbose_name_plural = "Міста"
        ordering = ['title', 'country']

    def __str__(self):
        return self.title


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name="Назва категорії")

    class Meta:
        verbose_name = "Категорії"
        verbose_name_plural = "Категорії"
        ordering = ['title', 'id']

    def __str__(self):
        return self.title


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name="Назва компанії")
    website_url = models.CharField(max_length=100, verbose_name="Адреса веб-сайту команії")
    workers_count = models.PositiveIntegerField(default=1, verbose_name="Кількість пацівників")
    description = models.TextField(max_length=100, verbose_name="Опис команії")
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE, verbose_name="Країна", default="Україна")
    city = models.ForeignKey(to=City, on_delete=models.CASCADE, verbose_name="Місто")
    address = models.CharField(max_length=100, verbose_name="Адреса")

    class Meta:
        verbose_name = "Компанії"
        verbose_name_plural = "Компанії"
        ordering = ['country', 'city', 'title']

    def __str__(self):
        return self.title


class Vacancy(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name="Назва вакансії")
    description = models.TextField(max_length=1000, verbose_name="Опис вакансії")
    slry_tps = [("HOURLY", "погодинно"), ("DAILY", "щоденно"), ("WEEKLY", "щотижня"), ("MONTHLY", "щомісячно")]
    salary_type = models.CharField(max_length=100, verbose_name="Тип оплати", choices=slry_tps)
    creation_date = models.DateTimeField(default=datetime.datetime.now(), verbose_name="Дата додавання")
    salary = models.PositiveIntegerField(verbose_name="Зарплата")
    crcy = [("₴", "HRYVNIA"), ("$", "DOLLAR"), ("€", "EURO")]
    currency = models.CharField(choices=crcy, max_length=10, verbose_name="Валюта")
    is_for_student = models.BooleanField(default=False, verbose_name="Для студентів")
    is_for_migrant = models.BooleanField(default=False, verbose_name="Для переселенців")
    edu_lvls = [("MIDDLE_SCHOOL", "Середня школа"), ("GRADUATE_SCHOOL", "Старша школа"), ("COLLEGE", "Коледж"),
                ("BACHELOR", "Бакалавр"), ("MASTER", "Магістр")]
    education_level = models.CharField(max_length=50, choices=edu_lvls, verbose_name="Освіта")
    exp_lvls = [("NONE", "Без досвіду"), ("HALF_YEAR", "Пів року"), ("ONE_MORE_YEAR", "Більше року"),
                ("TWO_MORE_YEAR", "Більше 2 років"), ("FIVE_MORE_YEAR", "Більше 5 років")]
    experience_level = models.CharField(max_length=50, choices=exp_lvls, verbose_name="Досвід")
    categories = models.ManyToManyField(to=Category, verbose_name="Категорія")
    company = models.ForeignKey(to=Company, on_delete=models.PROTECT, verbose_name="Компанія")

    class Meta:
        verbose_name = "Вакансії"
        verbose_name_plural = "Вакансії"
        ordering = ['company', 'salary']

    def __str__(self):
        return f'{self.title} у {self.company.city}'

    def get_curr(self):
        for currency in self.crcy:
            if currency[0] == self.currency:
                return currency[1]
