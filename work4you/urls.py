from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from work4you import settings
from work4you_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', get_vacancies),
    path('vacancy/<int:vacancy_id>', get_vacancy),
    path('vacancies/company/<int:company_id>', get_company_vacancies),
    path('find/vacancies', find_vacancies),
    path('company/<int:company_id>', get_company),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
