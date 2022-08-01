import datetime
from django.contrib.auth.models import AbstractUser
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
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE, verbose_name="Країна")

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


class EducationLevel(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name="Освіта", null=True)

    class Meta:
        verbose_name = "Рівень освіти"
        verbose_name_plural = "Рівень освіти"

    def __str__(self):
        return self.title


class ExperienceLevel(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name="Освіта", null=True)

    class Meta:
        verbose_name = "Рівень досвіду"
        verbose_name_plural = "Рівень досвіду"

    def __str__(self):
        return self.title


class Contacts(models.Model):
    id = models.AutoField(primary_key=True)
    phone1 = models.CharField(max_length=20, verbose_name="Телефон 1", null=True, blank=False)
    phone2 = models.CharField(max_length=20, verbose_name="Телефон 2", null=True, blank=True)
    email = models.CharField(max_length=30, verbose_name="Email", null=True, blank=False)

    class Meta:
        verbose_name = "Контакти компанії"
        verbose_name_plural = "Контакти компанії"
        ordering = ['id', 'email', 'phone1', 'phone2']

    def __str__(self):
        return f'{self.email}, тел.1 {self.phone1}, тел.2 {self.phone2}'


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name="Назва компанії")
    website_url = models.CharField(max_length=100, verbose_name="Адреса веб-сайту команії")
    wrkrs_cnt_choices = [('0–10', '0–10'), ('20–50', '20–50'), ('50–100', '50–100'), ('100–500', '100–500'),
                         ('500–1000+', '500–1000+')]
    workers_count = models.CharField(max_length=20, default="10-20", verbose_name="Кількість пацівників",
                                     choices=wrkrs_cnt_choices)
    description = models.TextField(max_length=1500, verbose_name="Опис команії")
    city = models.ForeignKey(to=City, on_delete=models.CASCADE, verbose_name="Місто")
    address = models.CharField(max_length=100, verbose_name="Адреса")
    image = models.ImageField(verbose_name="Логотип", upload_to="photos/%Y/%m/%d/", null=True, blank=True)
    categories = models.ManyToManyField(to=Category, verbose_name="Категорія", null=True, blank=True)
    contacts = models.OneToOneField(to=Contacts, on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name="Контакти")

    class Meta:
        verbose_name = "Компанії"
        verbose_name_plural = "Компанії"
        ordering = ['city', 'title']

    def __str__(self):
        return self.title


class Vacancy(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name="Назва вакансії")
    description = models.TextField(max_length=1500, verbose_name="Опис вакансії")
    creation_date = models.DateTimeField(default=datetime.datetime.now(), verbose_name="Дата додавання")
    salary = models.PositiveIntegerField(verbose_name="Зарплата (грн/міс.)")
    employment_types = models.ManyToManyField(to=EmploymentType, max_length=100, verbose_name="Тип зайнятості", null=True, blank=True)
    candidate_types = models.ManyToManyField(to=CandidateType, verbose_name="Типи кандидатів", null=True, blank=True)
    education_level = models.ForeignKey(to=EducationLevel, on_delete=models.CASCADE, verbose_name="Освіта", null=False, blank=True)
    experience_level = models.ForeignKey(to=ExperienceLevel, on_delete=models.CASCADE, verbose_name="Досвід", null=False, blank=True)
    categories = models.ManyToManyField(to=Category, verbose_name="Категорія")
    company = models.ForeignKey(to=Company, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Компанія")
    is_active = models.BooleanField(default=True, verbose_name="Активна вакансія")

    class Meta:
        verbose_name = "Вакансії"
        verbose_name_plural = "Вакансії"
        ordering = ['company', 'salary']

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        self.title = self.title.lower().capitalize()
        super().save(*args, **kwargs)


class Candidate(models.Model):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=30, null=True, verbose_name="Номер телефону")
    creation_date = models.DateTimeField(default=datetime.datetime.now(), verbose_name="Дата реєстрації")
    education_level = models.ForeignKey(to=EducationLevel, on_delete=models.CASCADE, verbose_name="Освіта", null=True, blank=False)
    experience_level = models.ForeignKey(to=ExperienceLevel, on_delete=models.CASCADE, verbose_name="Досвід", null=True, blank=True)
    image = models.ImageField(verbose_name="Ваше фото", upload_to="photos/%Y/%m/%d/", null=True, blank=True)
    saved_vacancies = models.ManyToManyField(to=Vacancy, null=True, verbose_name="Збережені вакансії", blank=True)
    desired_vacancy = models.CharField(max_length=100, null=True, blank=True, verbose_name="Бажана вакансія")
    desired_salary = models.PositiveIntegerField(default=7000, null=True, blank=True, verbose_name="Бажана зарплата (грн/міс.)")
    intro = models.TextField(max_length=2000, null=True, blank=True, verbose_name="Трохи про себе")
    city = models.ForeignKey(to=City, on_delete=models.CASCADE, verbose_name="Місто", null=True, blank=True)

    class Meta:
        verbose_name = "Кандидати"
        verbose_name_plural = "Кандидати"
        ordering = ['creation_date', 'id']

    def __str__(self):
        return f'{self.id}, бажана вакансія: {self.desired_vacancy}'


class Employer(models.Model):
    id = models.AutoField(primary_key=True)
    creation_date = models.DateTimeField(default=datetime.datetime.now(), verbose_name="Дата реєстрації")
    saved_candidates = models.ManyToManyField(to=Candidate, null=True, verbose_name="Збережені кандидати", blank=True)
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE, null=True, verbose_name="Компанія", blank=True)

    class Meta:
        verbose_name = "Роботодавці"
        verbose_name_plural = "Роботодавці"
        ordering = ['creation_date', 'id']

    def __str__(self):
        if self.company:
            return f'Компанія {self.company}, id = {self.company.id}'
        else:
            return f'Компанія не зареестрована.'


class User(AbstractUser):
    is_candidate = models.BooleanField(default=False, verbose_name="Кандидат")
    is_employer = models.BooleanField(default=False, verbose_name="Роботодавець")
    candidate = models.OneToOneField(to=Candidate, on_delete=models.CASCADE, null=True, blank=True)
    employer = models.OneToOneField(to=Employer, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Користувачі"
        verbose_name_plural = "Користувачі"
        ordering = ['id', 'first_name', 'last_name']

    def __str__(self):
        return f'{self.id}. {self.username}, {self.first_name} {self.last_name}'
