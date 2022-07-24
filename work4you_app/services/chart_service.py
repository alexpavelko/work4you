import json
import operator
import statistics

from work4you_app.models import Vacancy, City, Category, Candidate


def get_vacancy_count_data():
    cities = [city for city in City.objects.all() if city.title != "Вся країна"]
    chart_1_data = []
    for city in cities:
        chart_1_data.append({
            "name": city.title,
            "y": Vacancy.objects.filter(company__city=city).count(),
            "drilldown": city.title
        })
    chart_1_data.sort(key=operator.itemgetter("y"), reverse=True)
    chart_1_data = json.dumps(chart_1_data[0:5], sort_keys=True, ensure_ascii=False)
    return chart_1_data


def get_categories_data():
    categories = Category.objects.all()
    chart_2_data = []
    sum = 0
    for category in Category.objects.all():
        sum += Vacancy.objects.filter(categories__in=[category]).count()
    for category in categories:
        chart_2_data.append({
            "name": category.title,
            "y": Vacancy.objects.filter(categories__in=[category]).count() / sum * 100,
            "drilldown": category.title
        })

    chart_2_data.sort(key=operator.itemgetter("y"), reverse=True)
    chart_2_data = json.dumps(chart_2_data[0:5], sort_keys=True, ensure_ascii=False)
    return chart_2_data


def get_salary_data():
    chart_3_data = []
    vacancies = sorted(Vacancy.objects.all(), key=lambda v: v.salary, reverse=True)
    for vacancy in vacancies:
        mediana_vacancies = Vacancy.objects.filter(title=vacancy.title)
        mediana_salary = statistics.median(map(lambda v: v.salary, list(mediana_vacancies)))
        names = [elem["name"] for elem in chart_3_data]
        if vacancy.title not in names:
            chart_3_data.append({
                "name": vacancy.title,
                "y": mediana_salary,
                "drilldown": vacancy.title
            })
    chart_3_data = json.dumps(chart_3_data[:5], sort_keys=True, ensure_ascii=False)
    return chart_3_data


def get_candidates_edu_data():
    edu_lvls = list(map(lambda el: str(el[0]), Candidate.edu_lvls))
    sum = 0
    data = []
    for lvl in edu_lvls:
        sum += Candidate.objects.filter(education_level=lvl).count()
    for lvl in edu_lvls:
        count = Candidate.objects.filter(education_level=lvl).count()
        if count > 0:
            data.append({
                "name": lvl,
                "y": Candidate.objects.filter(education_level=lvl).count() / sum * 100,
                "drilldown": lvl
            })
    data.sort(key=operator.itemgetter("y"), reverse=True)
    data = json.dumps(data, sort_keys=True, ensure_ascii=False)
    return data


def get_candidates_exp_data():
    exp_lvls = list(map(lambda el: str(el[0]), Candidate.exp_lvls))
    sum = 0
    data = []
    for lvl in exp_lvls:
        sum += Candidate.objects.filter(experience_level=lvl).count()
    for lvl in exp_lvls:
        count = Candidate.objects.filter(experience_level=lvl).count()
        if count > 0:
            data.append({
                "name": lvl,
                "y": Candidate.objects.filter(experience_level=lvl).count() / sum * 100,
                "drilldown": lvl
            })
    data.sort(key=operator.itemgetter("y"), reverse=True)
    data = json.dumps(data, sort_keys=True, ensure_ascii=False)
    return data
