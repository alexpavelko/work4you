from django.contrib import admin
from django.forms import Textarea

from .models import *

formfield_overrides = {
    models.CharField: {'widget': Textarea(attrs={'rows': 1, 'cols': 50})},
    models.TextField: {'widget': Textarea(attrs={'rows': 15, 'cols': 100})},
}


class VacancyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'company', 'creation_date', 'salary', 'currency',
                    'is_for_student', 'is_for_migrant',)
    list_display_links = ('id', 'title', 'company')
    search_fields = ('is_for_student', 'is_for_migrant')
    list_editable = ('is_for_student', 'is_for_migrant')
    list_filter = ('salary', 'creation_date')
    formfield_overrides = formfield_overrides


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'website_url', 'description', 'workers_count', 'country', 'city', 'address')
    list_display_links = ('title', 'website_url', 'address')
    formfield_overrides = formfield_overrides


admin.site.register(Category)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Company, CompanyAdmin)
