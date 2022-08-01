from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import *


class CandidateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Candidate
        fields = '__all__'
        exclude = ['user', 'creation_date', 'saved_vacancies']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'intro': forms.Textarea(attrs={'cols': 100, 'rows': 20})
        }


class VacancyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Vacancy
        fields = '__all__'
        exclude = ['creation_date', 'company']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 100, 'rows': 20}),
            'categories': forms.SelectMultiple(attrs={'size': 10}),
            'candidate_types': forms.SelectMultiple(attrs={'size': 4}),
            'employment_types': forms.SelectMultiple(attrs={'size': 4}),
        }


class CompanyForm(forms.ModelForm):
    def __init__(self,  *args, **kwargs):
        self.path = kwargs.pop('path', None)
        super(CompanyForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Company
        fields = '__all__'
        exclude = ['contacts']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 100, 'rows': 20}),
            'categories': forms.SelectMultiple(attrs={'size': 10}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if 'edit' not in self.path and Company.objects.filter(title=title).count() > 0:
            raise ValidationError("Така компанія вже існує.")
        else:
            return title


class ContactsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Contacts
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 100, 'rows': 20})
        }


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label='Ім\'я', widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Прізвище', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).count() > 0:
            raise ValidationError("Користувач з такою електронною поштою вже існує.")
        else:
            return email


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

