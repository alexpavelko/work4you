import random
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from work4you_app.forms import *
from work4you_app.models import *


def get_candidates(request):
    page = {
        'candidates': User.objects.all(),
        'exp_lvls': map(lambda lvl: str(lvl[0]).capitalize(), Candidate.exp_lvls),
        'edu_lvls': map(lambda lvl: str(lvl[0]).capitalize(), Candidate.edu_lvls),
        'cities': City.objects.all()
    }
    return render(request, 'work4you_app/user/candidates.html', page)


def get_vacancies(request):
    count = Vacancy.objects.count()
    top3 = random.sample(list(Vacancy.objects.all()), 3)
    user = request.user
    if user.is_authenticated:
        if user.is_candidate:
            candidate = Candidate.objects.filter(user__id=user.id)[0]
    else:
        candidate = None
    page = {
        'title': f'{count} вакансій по Україні',
        'vacancies': Vacancy.objects.all(),
        'top3': top3,
        'categories': Category.objects.all(),
        'employment_types': EmploymentType.objects.all(),
        'currencies': Currency.objects.all(),
        'candidate_types': CandidateType.objects.all(),
        'cities': City.objects.all(),
        # 'candidate': candidate
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
    employment_types = list(map(lambda t: EmploymentType.objects.get(title=t), request.GET.getlist('employment_types')))
    candidate_types = list(map(lambda ct: CandidateType.objects.get(title=ct), request.GET.getlist('candidate_types')))
    categories = list(map(lambda c: Category.objects.get(title=c), request.GET.getlist('categories')))
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


def get_candidate(request, candidate_id):
    user = User.objects.get(candidate_id=candidate_id)
    page = {
        'user': user
    }
    return render(request, 'work4you_app/user/candidate.html', page)


def get_saved_vacancies(request, candidate_id):
    candidate = Candidate.objects.get(id=candidate_id)
    vacancies = candidate.saved_vacancies.all()
    top3 = sorted(Vacancy.objects.all()[:3], key=lambda x: random.random())
    page = {
        'title': 'Збережені вакансії',
        'vacancies': vacancies,
        'top3': top3,
        'categories': Category.objects.all(),
        'employment_types': EmploymentType.objects.all(),
        'currencies': Currency.objects.all(),
        'candidate_types': CandidateType.objects.all(),
        'cities': City.objects.all(),
        'candidate': candidate
    }
    return render(request, 'work4you_app/vacancy/vacancies.html', page)


def save_vacancy(request, candidate_id, vacancy_id):
    candidate = Candidate.objects.get(id=candidate_id)
    if request.method == 'GET':
        vacancy = Vacancy.objects.get(id=vacancy_id)
        candidate.saved_vacancies.add(vacancy)
        candidate.save()

    return redirect(request.META.get('HTTP_REFERER'))


def add_candidate(request):
    candidate_form = CandidateForm()
    if request.method == 'POST':
        candidate_form = CandidateForm(request.POST)
        if candidate_form.is_valid():
            candidate = candidate_form.save()
            user = request.user
            user.candidate = candidate
            user.candidate.image = request.FILES['image']
            candidate.save()
            user.save()

            return redirect(f'/candidate/{candidate.id}')
    page = {
        'title': 'Додати данні кандидата',
        'form': candidate_form,
    }
    return render(request, "work4you_app/form.html", page)


def add_company(request):
    company_form = CompanyForm()
    if request.method == 'POST':
        company_form = CompanyForm(request.POST)
        if company_form.is_valid():
            company = company_form.save()
            company.save()
            user = request.user
            user.employer.company = company
            user.employer.company.image = request.FILES['image']
            user.employer.company.save()
            user.employer.save()
            user.save()
            messages.success(request, 'Ви успішно зареєстрували компанію ' + company.title)
            return redirect(f'/company/{company.id}')

    page = {
        'title': 'Додати компанію',
        'form': company_form,
    }
    return render(request, "work4you_app/form.html", page)


def add_company_vacancy(request, company_id):
    vacancy_form = VacancyForm()
    if request.method == 'POST':
        vacancy_form = VacancyForm(request.POST)
        if vacancy_form.is_valid():
            vacancy = vacancy_form.save()
            vacancy.company = Company.objects.get(id=company_id)
            vacancy.save()
            return redirect(f'/company/{company_id}')
    page = {
        'title': 'Додати вакансію',
        'form': vacancy_form
    }
    return render(request, "work4you_app/form.html", page)


def add_contacts(request, company_id):
    contacts_form = ContactsForm()
    company = Company.objects.get(id=company_id)
    if request.method == 'POST':
        contacts_form = ContactsForm(request.POST)
        if contacts_form.is_valid():
            contacts = contacts_form.save()
            contacts.save()
            company.contacts = contacts
            company.save()
            return redirect(f'/company/{company_id}')
    page = {
        'title': f'Додати контакти до команії {company.title}',
        'form': contacts_form
    }
    return render(request, "work4you_app/form.html", page)


def registerPage(request):
    form = RegisterUserForm()
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            candidate = Candidate.objects.create(user=user)
            candidate.save()
            employer = Employer.objects.create(user=user)
            employer.save()
            user.candidate = candidate
            user.employer = employer
            user.save()
            messages.success(request, 'Ви успішно зареєструвалися як ' + username)
            return redirect('/login')

    page = {'form': form}
    return render(request, 'work4you_app/user/auth/register.html', page)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.POST.get('candidate') is not None:
                user.is_candidate = True
                user.is_employer = False
                user.save()
                if user.candidate.desired_vacancy is None:
                    return redirect('/candidate/add')
                return redirect('/vacancies')
            else:
                user.is_employer = True
                user.is_candidate = False
                user.save()
                if user.employer.company is None:
                    return redirect('/company/add')
                return redirect(f'/company/{user.employer.company.id}')
        else:
            messages.add_message(request, messages.ERROR, 'Ім\'я користувача або пароль некоректні')
    page = {}
    return render(request, 'work4you_app/user/auth/login.html', page)


def logoutUser(request):
    logout(request)
    return redirect('login')
