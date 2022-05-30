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


class Currency(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name="Валюта")

    class Meta:
        verbose_name = "Валюти"
        verbose_name_plural = "Валюти"
        ordering = ['-title', 'id']

    def __str__(self):
        return self.title


class CandidateType(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name="Тип кандидата")

    class Meta:
        verbose_name = "Типи кандидатів"
        verbose_name_plural = "Типи кандидатів"
        ordering = ['title', 'id']

    def __str__(self):
        return self.title


class EmploymentType(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name="Тип зайнятості")

    class Meta:
        verbose_name = "Типи зайнятості"
        verbose_name_plural = "Типи зайнятості"
        ordering = ['title', 'id']

    def __str__(self):
        return self.title


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name="Назва компанії")
    website_url = models.CharField(max_length=100, verbose_name="Адреса веб-сайту команії")
    wrkrs_cnt_choices = [('0–10', '0–10'), ('20–50', '20–50'), ('50–100', '50–100'), ('100–500', '100–500'), ('500–1000+', '500–1000+')]
    workers_count = models.CharField(max_length=20, default="10-20", verbose_name="Кількість пацівників", choices=wrkrs_cnt_choices)
    description = models.TextField(max_length=1500, verbose_name="Опис команії")
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE, verbose_name="Країна", default="Україна")
    city = models.ForeignKey(to=City, on_delete=models.CASCADE, verbose_name="Місто")
    address = models.CharField(max_length=100, verbose_name="Адреса")
    image = models.ImageField(verbose_name="Компания", upload_to="photos/%Y/%m/%d/", null=True, blank=True)
    categories = models.ManyToManyField(to=Category, verbose_name="Категорія", null=True, blank=True)

    class Meta:
        verbose_name = "Компанії"
        verbose_name_plural = "Компанії"
        ordering = ['country', 'city', 'title']

    def __str__(self):
        return self.title


class Vacancy(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name="Назва вакансії")
    description = models.TextField(max_length=1500, verbose_name="Опис вакансії")
    employment_type = models.ForeignKey(to=EmploymentType, on_delete=models.CASCADE,
                                        max_length=100, verbose_name="Тип зайнятості")
    creation_date = models.DateTimeField(default=datetime.datetime.now(), verbose_name="Дата додавання")
    salary = models.PositiveIntegerField(verbose_name="Зарплата")
    currency = models.ForeignKey(to=Currency, on_delete=models.CASCADE, max_length=15, verbose_name="Валюта", default="грн")
    candidate_types = models.ManyToManyField(to=CandidateType, verbose_name="Типи кандидатів", null=True, blank=True)
    edu_lvls = [("середня школа", "середня школа"), ("старша школа", "старша школа"), ("коледж", "коледж"),
                ("бакалавр", "бакалавр"), ("магістр", "магістр")]
    education_level = models.CharField(max_length=50, choices=edu_lvls, verbose_name="Освіта")
    exp_lvls = [("без досвіду", "без досвіду"), ("пів року", "пів року"), ("більше року", "більше року"),
                ("більше 2 років", "більше 2 років"), ("більше 5 років", "більше 5 років")]
    experience_level = models.CharField(max_length=50, choices=exp_lvls, verbose_name="Досвід")
    categories = models.ManyToManyField(to=Category, verbose_name="Категорія")
    company = models.ForeignKey(to=Company, on_delete=models.PROTECT, verbose_name="Компанія")

    class Meta:
        verbose_name = "Вакансії"
        verbose_name_plural = "Вакансії"
        ordering = ['company', 'salary']

    def __str__(self):
        return f'{self.title} у {self.company.city}'

    def save(self, *args, **kwargs):
        self.title = self.title.lower().capitalize()
        super().save(*args, **kwargs)

    def get_currency_sign(self):
        if str(self.currency) == 'грн':
            return "fa-solid fa-hryvnia-sign"
        elif str(self.currency) == 'usd':
            return "fa-solid fa-usd"
        elif str(self.currency) == 'eur':
            return "fa-solid fa-eur"


