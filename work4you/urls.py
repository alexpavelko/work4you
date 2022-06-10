from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from work4you import settings
from work4you_app.views import *

urlpatterns = [
      path('admin/', admin.site.urls),

      path('register/', registerPage, name="register"),
      path('login/', loginPage, name="login"),
      path('logout/', logoutUser, name="logout"),

      path('', get_vacancies),
      path('vacancies', get_vacancies),
      path('vacancy/<int:vacancy_id>', get_vacancy),

      path('vacancies/company/<int:company_id>', get_company_vacancies),
      path('vacancies/find', find_vacancies),

      path('company/<int:company_id>', get_company),
      path('company/add', add_company),
      path('company/<int:company_id>/vacancy/add', add_company_vacancy),

      path('candidates', get_candidates),
      path('candidate/<int:candidate_id>', get_candidate),
      path('candidate/add', add_candidate),
      path('candidate/<int:candidate_id>/vacancy/<int:vacancy_id>/save', save_vacancy),
      path('candidate/<int:candidate_id>/vacanices/saved', get_saved_vacancies),

      path('company/<int:company_id>/contacts/add', add_contacts),

  ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
