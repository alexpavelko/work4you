import sweetify
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect

from work4you_app.forms import RegisterUserForm
from work4you_app.models import Employer, Candidate


def register_user(request):
    form = RegisterUserForm()
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            candidate = Candidate.objects.create(user=user)
            candidate.save()
            employer = Employer.objects.create(user=user)
            employer.save()
            user.candidate = candidate
            user.employer = employer
            user.save()
            sweetify.success(request, f'Ви успішно зареєструвалися як {username}')
            return redirect('/login')

    context = {'form': form}
    return render(request, 'work4you_app/user/auth/register.html', context)


def login_user(request):
    if request.user.is_authenticated:
        logout(request)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.POST.get('candidate') is not None:
                user.is_candidate = True
                user.is_employer = False
                user.save()
                sweetify.success(request, f'Ви успішно увійшли до профілю кандидата {username}')
                if user.candidate.desired_vacancy is None:
                    return redirect('/candidate/add')
                return redirect('/vacancies')
            else:
                user.is_employer = True
                user.is_candidate = False
                user.save()
                if user.employer.company is None:
                    return redirect('/company/add')
                return redirect(f'/company/{user.employer.company.id}')
        else:
            sweetify.error(request, 'Ім\'я користувача або пароль некоректні')

    return render(request, 'work4you_app/user/auth/login.html')


def logout_user(request):
    logout(request)
    return redirect('/login')
