from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from work4you import settings
from work4you_app.services.auth_service import *
from work4you_app.views import *

urlpatterns = [
      path('admin/', admin.site.urls),

      path('register/', register_user),
      path('login/', login_user),
      path('logout/', logout_user),

      path('', get_vacancies),
      path('vacancies', get_vacancies),
      path('vacancies/find', find_vacancies),
      path('vacancy/<int:vacancy_id>', get_vacancy),
      path('vacancy/<int:vacancy_id>/edit', edit_vacancy),
      path('vacancy/<int:vacancy_id>/change_activity', change_vacancy_activity),

      path('company/<int:company_id>', get_company),
      path('company/add', add_company),
      path('company/<int:company_id>/vacancy/add', add_company_vacancy),
      path('company/<int:company_id>/vacancy/<int:vacancy_id>/delete', delete_vacancy),

      path('candidates', get_candidates),
      path('candidates/find', find_candidates),
      path('candidate/<int:candidate_id>', get_candidate),
      path('candidate/add', add_candidate),
      path('candidate/<int:candidate_id>/edit', edit_candidate),
      path('candidate/<int:candidate_id>/vacancy/<int:vacancy_id>/save', save_candidate_vacancy),
      path('candidate/<int:candidate_id>/vacancy/<int:vacancy_id>/delete', delete_candidate_vacancy),
      path('candidate/<int:candidate_id>/vacancies/saved', get_saved_vacancies),

      path('company/<int:company_id>/contacts/add', add_or_edit_contacts),
      path('company/<int:company_id>/contacts/edit', add_or_edit_contacts),
      path('company/<int:company_id>/edit', edit_company),
      path('charts/<slug:type>', get_charts)

      ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
