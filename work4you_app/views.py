import random

import sweetify as sweetify
from django.shortcuts import render, redirect

from work4you_app.forms import *
from work4you_app.models import *
from work4you_app.services import chart_service, vacancy_service
from work4you_app.services.vacancy_service import initialize_vacancyForm


def get_vacancies(request):
    vacancies = Vacancy.objects.filter(is_active=True)
    if vacancies.count() >= 3:
        top3 = random.sample(list(vacancies), 3)
    else:
        top3 = None
    context = {
        'title': f'{vacancies.count()} вакансій по Україні',
        'salary': 0,
        'vacancies': vacancies,
        'top3': top3,
        'categories': Category.objects.all(),
        'employment_types': EmploymentType.objects.all(),
        'candidate_types': CandidateType.objects.all(),
        'cities': City.objects.all(),
        'selected_city': 'Вся країна',
        'salary_data': chart_service.get_salary_data(),
    }
    return render(request, "work4you_app/vacancy/vacancies.html", context)


def get_vacancy(request, vacancy_id):
    vacancy = Vacancy.objects.get(id=vacancy_id)
    context = {
        'vacancy': vacancy,
        'title': vacancy
    }
    return render(request, "work4you_app/vacancy/vacancy.html", context)


def delete_vacancy(request, company_id, vacancy_id):
    Vacancy.objects.get(id=vacancy_id).delete()
    try:
        Vacancy.objects.get(id=vacancy_id)
        sweetify.error(request, 'Не вдалося видалити вакансію')
        return redirect(request.META.get('HTTP_REFERER'))
    except Vacancy.DoesNotExist:
        sweetify.success(request, 'Вакансію видалено')
        return redirect(f'/company/{company_id}')


def edit_vacancy(request, vacancy_id):
    vacancy = Vacancy.objects.get(id=vacancy_id)
    vacancy_form = initialize_vacancyForm(vacancy)
    if request.method == 'POST':
        vacancy_form = VacancyForm(request.POST)
        if vacancy_form.is_valid():
            vacancy = vacancy_service.get_vacancyForm_data(vacancy, vacancy_form)
            vacancy.save()
            sweetify.success(request, 'Ви успішно оновили інформацію про вакансію ' + vacancy.title)
            return redirect(f'/vacancy/{vacancy.id}')
    context = {
        'title': 'Відредагувати мою вакансію',
        'confirm_button': 'Відредагувати',
        'form': vacancy_form,
    }
    return render(request, "work4you_app/form.html", context)


def find_vacancies(request):
    context = vacancy_service.find_vacancies(request)
    return render(request, "work4you_app/vacancy/vacancies.html", context)


def get_company(request, company_id):
    context = {
        'title': Company.objects.get(id=company_id).title,
        'company': Company.objects.get(id=company_id),
        'vacancies': Vacancy.objects.filter(company=Company.objects.get(id=company_id))
    }
    return render(request, "work4you_app/company/company.html", context)


def change_vacancy_activity(request, vacancy_id):
    vacancy = Vacancy.objects.get(id=vacancy_id)
    vacancy.is_active = not vacancy.is_active
    vacancy.save()
    if vacancy.is_active:
        sweetify.toast(request, "Вакансія буде відображатися у списку вакансій")
    else:
        sweetify.toast(request, "Вакансію приховано")
    return redirect(f'/company/{vacancy.company.id}#vacancies')


def find_candidates(request):
    candidates = Candidate.objects.filter(desired_salary__gte=request.GET.get('desired_salary'),
                                          education_level__in=request.GET.getlist('edu_lvls'),
                                          experience_level__in=request.GET.getlist('exp_lvls'),
                                          city__in=request.GET.get('city'),
                                          desired_vacancy__contains=request.GET.get('query')
                                          ).distinct()
    context = {
        'title': f'Знайдено {candidates.count()} кандидатів',
        'desired_salary': request.GET.get('desired_salary'),
        'edu_lvls': EducationLevel.objects.all(),
        'exp_lvls': ExperienceLevel.objects.all(),
        'candidates': candidates,
        'cities': City.objects.all(),
        'selected_query': request.GET.get('query'),
        'selected_city': request.GET.get('city'),
        'selected_exp_lvls': request.GET.get('exp_lvls'),
        'selected_edu_lvls': request.GET.get('edu_lvls'),
    }
    return render(request, 'work4you_app/user/candidates.html', context)


def get_candidate(request, candidate_id):
    candidate = Candidate.objects.get(id=candidate_id)
    user = User.objects.get(candidate_id=candidate_id)
    context = {
        'candidate_email': user.email,
        'candidate_first_name': user.first_name,
        'candidate_last_name': user.last_name,
        'candidate': candidate
    }
    return render(request, 'work4you_app/user/candidate.html', context)


def get_saved_vacancies(request, candidate_id):
    candidate = Candidate.objects.get(id=candidate_id)
    context = {
        'title': 'Збережені вакансії',
        'salary': 0,
        'vacancies': candidate.saved_vacancies.all(),
        'top3': sorted(Vacancy.objects.all()[:3], key=lambda x: random.random()),
        'categories': Category.objects.all(),
        'employment_types': EmploymentType.objects.all(),
        'candidate_types': CandidateType.objects.all(),
        'cities': City.objects.all(),
        'candidate': candidate
    }
    return render(request, 'work4you_app/vacancy/vacancies.html', context)


def save_candidate_vacancy(request, candidate_id, vacancy_id):
    candidate = Candidate.objects.get(id=candidate_id)
    if request.method == 'GET':
        vacancy = Vacancy.objects.get(id=vacancy_id)
        candidate.saved_vacancies.add(vacancy)
        candidate.save()

    return redirect(request.META.get('HTTP_REFERER'))


def delete_candidate_vacancy(request, candidate_id, vacancy_id):
    candidate = Candidate.objects.get(id=candidate_id)
    if request.method == 'GET':
        vacancy = Vacancy.objects.get(id=vacancy_id)
        candidate.saved_vacancies.remove(vacancy)
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
    context = {
        'title': 'Додати данні кандидата',
        'confirm_button': 'Додати',
        'form': candidate_form,
    }
    return render(request, "work4you_app/form.html", context)


def edit_candidate(request, candidate_id):
    candidate = Candidate.objects.get(id=candidate_id)
    candidate_form = CandidateForm(initial={
        'phone': candidate.phone,
        'education_level': candidate.education_level,
        'experience_level': candidate.experience_level,
        'image': candidate.image,
        'desired_vacancy': candidate.desired_vacancy,
        'desired_salary': candidate.desired_salary,
        'intro': candidate.intro,
        'city': candidate.city,
    })
    if request.method == 'POST':
        candidate_form = CandidateForm(data=request.POST, files=request.FILES)
        if candidate_form.is_valid():
            Candidate.objects.filter(id=candidate_id).update(
                phone=candidate_form.cleaned_data['phone'],
                education_level=candidate_form.cleaned_data['education_level'],
                experience_level=candidate_form.cleaned_data['experience_level'],
                desired_vacancy=candidate_form.cleaned_data['desired_vacancy'],
                desired_salary=candidate_form.cleaned_data['desired_salary'],
                intro=candidate_form.cleaned_data['intro'],
                city=candidate_form.cleaned_data['city'],
            )
            if request.FILES.get('image') is not None:
                candidate.image = request.FILES.get('image')
                candidate.save()
            return redirect(f'/candidate/{candidate.id}')
    context = {
        'title': 'Відредагувати мої дані',
        'confirm_button': 'Відредаувати',
        'form': candidate_form,
    }
    return render(request, "work4you_app/form.html", context)


def add_company(request):
    company_form = CompanyForm()
    if request.method == 'POST':
        company_form = CompanyForm(request.POST, path=request.path)
        if company_form.is_valid():
            company = company_form.save()
            company.save()
            user = request.user
            user.employer.company = company
            if request.FILES.get('image') is not None:
                user.employer.company.image = request.FILES['image']
            user.employer.company.save()
            user.employer.save()
            user.save()
            sweetify.success(request, f'Ви успішно зареєстрували компанію {company.title}')
            return redirect(f'/company/{company.id}')
    context = {
        'title': 'Додати компанію',
        'confirm_button': 'Додати',
        'form': company_form,
    }
    return render(request, "work4you_app/form.html", context)


def add_company_vacancy(request, company_id):
    vacancy_form = VacancyForm()
    if request.method == 'POST':
        vacancy_form = VacancyForm(request.POST)
        if vacancy_form.is_valid():
            vacancy = vacancy_form.save()
            vacancy.company = Company.objects.get(id=company_id)
            vacancy.save()
            return redirect(f'/company/{company_id}')
    context = {
        'title': 'Додати вакансію',
        'confirm_button': 'Додати',
        'form': vacancy_form
    }
    return render(request, "work4you_app/form.html", context)


def edit_company(request, company_id):
    company = Company.objects.get(id=company_id)
    company_form = CompanyForm(initial={
        'title': company.title,
        'contacts': company.contacts,
        'image': company.image,
        'city': company.city,
        'categories': company.categories.all(),
        'address': company.address,
        'description': company.description,
        'website_url': company.website_url,
        'workers_count': company.workers_count,
    }, path=request.path)
    if request.method == 'POST':
        company_form = CompanyForm(request.POST, path=request.path)
        if company_form.is_valid():
            company.title = company_form.cleaned_data['title']
            company.workers_count = company_form.cleaned_data['workers_count']
            company.website_url = company_form.cleaned_data['website_url']
            company.description = company_form.cleaned_data['description']
            company.address = company_form.cleaned_data['address']
            company.city = company_form.cleaned_data['city']
            if request.FILES.get('image') is not None:
                company.image = request.FILES.get('image')
            company.categories.set(company_form.cleaned_data.get('categories'))
            company.save()
            sweetify.success(request, 'Ви успішно оновили інформацію про компанію ' + company.title)
            return redirect(f'/company/{company.id}')
    context = {
        'title': 'Відредагувати мою компанію',
        'confirm_button': 'Відредагувати',
        'form': company_form,
    }
    return render(request, "work4you_app/form.html", context)


def add_or_edit_contacts(request, company_id):
    company = Company.objects.get(id=company_id)
    if company.contacts is None:
        title = f'Додати контакти для команії {company.title}'
        confirm_button = 'Додати'
        contacts_form = ContactsForm()
    else:
        title = f'Змінити контакти для команії {company.title}'
        confirm_button = 'Відредагувати'
        contacts_form = ContactsForm(initial={
            'email': company.contacts.email,
            'phone1': company.contacts.phone1,
            'phone2': company.contacts.phone2
        })
    if request.method == 'POST':
        contacts_form = ContactsForm(request.POST)
        if contacts_form.is_valid():
            company.contacts = contacts_form.save()
            company.save()
            return redirect(f'/company/{company_id}')
    context = {
        'title': title,
        'confirm_button': confirm_button,
        'form': contacts_form
    }
    return render(request, "work4you_app/form.html", context)


def get_candidates(request):
    candidates = Candidate.objects.all().exclude(desired_vacancy=None)
    context = {
        'title': f'{candidates.count()} кандидатів по Україні',
        'candidates': candidates,
        'edu_lvls': EducationLevel.objects.all(),
        'exp_lvls': ExperienceLevel.objects.all(),
        'desired_salary': 0,
        'cities': City.objects.all(),
        'edu_data': chart_service.get_candidates_edu_data(),
        'exp_data': chart_service.get_candidates_exp_data()
    }
    return render(request, 'work4you_app/user/candidates.html', context)


def get_charts(request, type):
    context = {}
    if type == "vacancies":
        context = {
            'title': 'Статистика вакансій',
            'vacancy_count_data': chart_service.get_vacancy_count_data(),
            'categories_data': chart_service.get_categories_data(),
            'salary_data': chart_service.get_salary_data(),
        }
    elif type == "candidates":
        context = {
            'title': 'Статистика кандидтів',
            'edu_data': chart_service.get_candidates_edu_data(),
            'exp_data': chart_service.get_candidates_exp_data()
        }
    return render(request, 'work4you_app/charts.html', context)
