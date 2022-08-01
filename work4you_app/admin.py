from django.contrib import admin
from django.forms import Textarea
from .models import *

formfield_overrides = {
    models.CharField: {'widget': Textarea(attrs={'rows': 1, 'cols': 50})},
    models.TextField: {'widget': Textarea(attrs={'rows': 15, 'cols': 60})},
}


class VacancyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'company', 'creation_date', 'salary',)
    list_display_links = ('id', 'title', 'company')
    list_filter = ('salary', 'creation_date')
    formfield_overrides = formfield_overrides
    filter_horizontal = ('categories', 'candidate_types', 'employment_types',)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'website_url', 'description', 'workers_count', 'city', 'address')
    list_display_links = ('title', 'website_url', 'address')
    formfield_overrides = formfield_overrides
    filter_horizontal = ('categories',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title',)
    formfield_overrides = formfield_overrides


class ContactsAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone1', 'phone2')
    list_display_links = ('id', 'email')


class EmployerAdmin(admin.ModelAdmin):
    list_display = ('id', 'creation_date', 'company')
    list_display_links = ('id', 'company')


class CandidateAdmin(admin.ModelAdmin):
    list_display = ('id', 'creation_date', 'phone', 'education_level', 'experience_level', 'desired_vacancy', 'city')
    list_display_links = ('id', 'phone')
    list_filter = ('phone', 'desired_vacancy', 'city')
    formfield_overrides = formfield_overrides


admin.site.register(User)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(CandidateType)
admin.site.register(EmploymentType)
admin.site.register(EducationLevel)
admin.site.register(ExperienceLevel)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Contacts, ContactsAdmin)
admin.site.register(Candidate)
admin.site.register(Employer, EmployerAdmin)

