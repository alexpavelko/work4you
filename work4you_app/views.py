from django.shortcuts import render

from work4you_app.models import Vacancy, Company


def get_vacancies(request):
    page = {
        'vacancies': Vacancy.objects.all()
    }
    return render(request, "work4you_app/vacancies.html", page)


def get_vacancy(request, vacancy_id):
    vacancy = Vacancy.objects.get(id=vacancy_id)
    page = {
        'vacancy': vacancy,
        'title': vacancy.title
    }
    return render(request, "work4you_app/vacancy.html", page)


def find_vacancies(request):
    page = {
        'vacancies': Vacancy.objects.all()
    }
    return render(request, "work4you_app/vacancies.html", page)


def get_company(request, company_id):
    page = {
        'vacancy': Company.objects.get(id=company_id)
    }
    return render(request, "work4you_app/company.html", page)
