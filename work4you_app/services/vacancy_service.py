from work4you_app.forms import VacancyForm
from work4you_app.models import Category, Vacancy, EmploymentType, CandidateType, City


def initialize_vacancyForm(vacancy):
    vacancy_form = VacancyForm(initial={
        'title': vacancy.title,
        'description': vacancy.description,
        'salary': vacancy.salary,
        'employment_types': vacancy.employment_types.all(),
        'candidate_types': vacancy.candidate_types.all(),
        'education_level': vacancy.education_level,
        'experience_level': vacancy.experience_level,
        'categories': vacancy.categories.all(),
    })
    return vacancy_form


def get_vacancyForm_data(vacancy, vacancy_form):
    vacancy.title = vacancy_form.cleaned_data['title']
    vacancy.description = vacancy_form.cleaned_data['description']
    vacancy.salary = vacancy_form.cleaned_data['salary']
    vacancy.employment_types.set = vacancy_form.cleaned_data.get('employment_types')
    vacancy.candidate_types.set = vacancy_form.cleaned_data.get('candidate_types')
    vacancy.categories.set = vacancy_form.cleaned_data.get('categories')
    vacancy.education_level = vacancy_form.cleaned_data['education_level']
    vacancy.experience_level = vacancy_form.cleaned_data['experience_level']
    return vacancy


def find_vacancies(request):
    query = request.GET.get('query').lower()
    city = City.objects.get(title=request.GET.get('city'))
    cities = [city]
    salary = request.GET.get('salary')
    if not salary:
        salary = 0
    employment_types = list(map(lambda t: EmploymentType.objects.get(title=t), request.GET.getlist('employment_types')))
    candidate_types = list(map(lambda ct: CandidateType.objects.get(title=ct), request.GET.getlist('candidate_types')))
    categories = list(map(lambda c: Category.objects.get(title=c), request.GET.getlist('categories')))
    if city.title == 'Вся країна':
        cities = City.objects.all()
    if not employment_types:
        employment_types = EmploymentType.objects.all()
    if not categories:
        categories = Category.objects.all()
    if not candidate_types:
        candidate_types = CandidateType.objects.all()
    vacancies = Vacancy.objects.filter(
        categories__in=categories, salary__gte=salary, employment_types__in=employment_types,
        candidate_types__in=candidate_types, company__city__in=cities, title__contains=query, is_active=True,
    ).distinct()
    context = {
        'title': f'Знайдено {vacancies.count()} вакансій',
        'salary': salary,
        'vacancies': vacancies,
        'categories': Category.objects.all(),
        'employment_types': EmploymentType.objects.all(),
        'candidate_types': CandidateType.objects.all(),
        'cities': City.objects.all(),
        'selected_query': query,
        'selected_city': city,
        'selected_employment_types': employment_types,
        'selected_candidate_types': candidate_types,
        'selected_categories': categories,
    }
    return context
