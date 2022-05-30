from django.shortcuts import render

from work4you_app.models import Vacancy, Company, Category, EmploymentType, Currency, CandidateType, City


def get_vacancies(request):
    count = Vacancy.objects.count()
    page = {
        'title': f'{count} вакансій по Україні',
        'vacancies': Vacancy.objects.all(),
        'categories': Category.objects.all(),
        'employment_types': EmploymentType.objects.all(),
        'currencies': Currency.objects.all(),
        'candidate_types': CandidateType.objects.all(),
        'cities': City.objects.all()
    }
    return render(request, "work4you_app/vacancy/vacancies.html", page)


def get_vacancy(request, vacancy_id):
    vacancy = Vacancy.objects.get(id=vacancy_id)
    page = {
        'vacancy_details': vacancy,
        'title': vacancy
    }
    return render(request, "work4you_app/vacancy/vacancy.html", page)


def find_vacancies(request):
    query = request.GET.get('query').lower()
    city = City.objects.get(title=request.GET.get('city'))
    cities = [city]
    salary = request.GET.get('salary')
    employment_types = list(
        map(lambda type: EmploymentType.objects.get(title=type), request.GET.getlist('employment_types')))
    candidate_types = list(map(lambda candidate_type: CandidateType.objects.get(title=candidate_type),
                               request.GET.getlist('candidate_types')))
    categories = list(map(lambda category: Category.objects.get(title=category), request.GET.getlist('categories')))
    currency = Currency.objects.get(title=request.GET.get('user_currency'))
    if city.title == 'Вся країна':
        cities = City.objects.all()
    if not employment_types:
        employment_types = EmploymentType.objects.all()
    if not categories:
        categories = Category.objects.all()
    if not candidate_types:
        candidate_types = CandidateType.objects.all()
    vacancies = Vacancy.objects.filter(
        categories__in=categories, salary__gte=salary, currency=currency,
        employment_type__in=employment_types, candidate_types__in=candidate_types,
        company__city__in=cities, title__contains=query).distinct()
    count = Vacancy.objects.count()
    page = {
        'title': f'{count} вакансій по Україні',
        'vacancies': vacancies,
        'categories': Category.objects.all(),
        'employment_types': EmploymentType.objects.all(),
        'currencies': Currency.objects.all(),
        'candidate_types': CandidateType.objects.all(),
        'cities': City.objects.all(),
        'selected_query': query,
        'selected_city': city,
        'selected_salary': salary,
        'selected_employment_types': employment_types,
        'selected_candidate_types': candidate_types,
        'selected_categories': categories,
        'selected_currency': currency
    }
    return render(request, "work4you_app/vacancy/vacancies.html", page)


def get_company(request, company_id):
    page = {
        'title': Company.objects.get(id=company_id).title,
        'company': Company.objects.get(id=company_id),
        'vacancies': Vacancy.objects.filter(company=Company.objects.get(id=company_id))
    }
    return render(request, "work4you_app/company/company.html", page)


def get_companies(request):
    page = {
        'companies': Company.objects.all()
    }
    return render(request, "work4you_app/company/company.html", page)


def get_company_vacancies(request, company_id):
    page = {
        'vacancies': Vacancy.objects.filter(company=Company.objects.get(id=company_id))
    }
    return render(request, "work4you_app/company/company.html", page)
