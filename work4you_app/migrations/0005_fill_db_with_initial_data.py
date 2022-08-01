from django.db import migrations

from work4you_app.models import Country


def countries_init(apps, schema_editor):
    Country = apps.get_model("work4you_app", "Country")
    if Country.objects.all().count() == 0:
        country = Country(title="Україна")
        country.save()


def cities_init(apps, schema_editor):
    cities = ["Вся країна", "Запоріжжя", "Київ", "Дніпро", "Одеса", "Львів"]
    City = apps.get_model("work4you_app", "City")
    Country = apps.get_model("work4you_app", "Country")
    if City.objects.all().count() == 0:
        for c in cities:
            city = City.objects.create(title=c, country=Country.objects.get(title="Україна"))


def categories_init(apps, schema_editor):
    categories = ["IT; програмування", "Маркетинг; реклама", "Банк; фінанси", "Спорт; фітнес",
                  "Сфера обслуговування", "Волонтерство", "Телекомунікації та зв'язок", "Дизайн; творчість",
                  "Управління персоналом", "Менеджмент; керівництво; адміністрація"]
    Category = apps.get_model("work4you_app", "Category")
    if Category.objects.all().count() == 0:
        for c in categories:
            category = Category(title=c)
            category.save()


def education_levels_init(apps, schema_editor):
    levels = ["Середня школа", "Старша школа", "Коледж", "Бакалавр", "Магістр"]
    EducationLevel = apps.get_model("work4you_app", "EducationLevel")
    if EducationLevel.objects.all().count() == 0:
        for el in levels:
            education_level = EducationLevel(title=el)
            education_level.save()


def experience_levels_init(apps, schema_editor):
    levels = ["Без досвіду", "Пів року", "Більше року", "Більше 2 років", "Більше 5 років"]
    ExperienceLevel = apps.get_model("work4you_app", "ExperienceLevel")
    if ExperienceLevel.objects.all().count() == 0:
        for el in levels:
            experience_level = ExperienceLevel(title=el)
            experience_level.save()


def employment_types_init(apps, schema_editor):
    types = ["Повна зайнятість", "Неповна зайнятість", "Дистанційна робота", "Стажування"]
    EmploymentType = apps.get_model("work4you_app", "EmploymentType")
    if EmploymentType.objects.all().count() == 0:
        for t in types:
            employment_type = EmploymentType(title=t)
            employment_type.save()


def candidate_types_init(apps, schema_editor):
    types = ["Студент", "Без досвіду", "Переселенець", "Пенсіонер"]
    CandidateType = apps.get_model("work4you_app", "CandidateType")
    if CandidateType.objects.all().count() == 0:
        for t in types:
            candidate_type = CandidateType(title=t)
            candidate_type.save()


class Migration(migrations.Migration):

    dependencies = [
        ('work4you_app', '0004_educationlevel_experiencelevel_and_more'),
    ]

    operations = [
        migrations.RunPython(countries_init),
        migrations.RunPython(cities_init),
        migrations.RunPython(categories_init),
        migrations.RunPython(education_levels_init),
        migrations.RunPython(experience_levels_init),
        migrations.RunPython(employment_types_init),
        migrations.RunPython(candidate_types_init),
    ]