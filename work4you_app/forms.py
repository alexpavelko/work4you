from django import forms
from .models import Vacancy


class VacancyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Vacancy
        fields = ['employment_type', 'categories', 'salary', 'currency', ]