from django.contrib import admin
from django.urls import path

from work4you_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', get_vacancies),
    path('vacancy/<int:vacancy_id>', get_vacancy),
    path('find/vacancies', find_vacancies),
    path('company/<int:company_id>', get_company),
]
