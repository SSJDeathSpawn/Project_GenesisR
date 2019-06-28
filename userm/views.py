from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, settings, get_user_model
from django.db.models import Model
from django.views.generic.detail import DetailView 

from .forms import LoginForm, UserSignUpForm
from .models import UserExtendedR

def user_login(request):
    if(request.method == 'POST'):
        form = LoginForm(request.POST)
        if(form.is_valid()):
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'userm/login.html', {'form': form})

def user_signup(request):
    if(request.method == 'POST'):
        form = UserSignUpForm(request.POST)
        if(form.is_valid()):
            cd = form.cleaned_data
            if cd['password1'] == cd['password2']:
                user = authenticate(username=cd['username'],
                                password=cd['password1'],
                                email=cd['email'])
                if user is None:
                    try:
                        UserExtendedR.objects.get(username=cd['username'])
                    except(KeyError, UserExtendedR.DoesNotExist):
                        try:
                            UserExtendedR.objects.get(email=cd['email'])
                        except(KeyError, UserExtendedR.DoesNotExist):
                            username = cd['username']
                            password1 = cd['password1']
                            password2 = cd['password2']
                            email = cd['email']
                            user = UserExtendedR.objects.create_user(username=username, email=email, password=password1)
                            return HttpResponse('User created successfully!')
                        else:
                            return HttpResponse('This email id is already registered!')
                    else:
                        return HttpResponse('Someone else has already taken the ID!')
            else:
                return HttpResponse('The passwords do not match!')
    else:
        form = UserSignUpForm()
    return render(request, 'userm/signup.html', {'form': form})

def user_details(request, username):
    try:
        user = UserExtendedR.objects.get(username=username)
    except(KeyError, UserExtendedR.DoesNotExist):
        return HttpResponse('User does not exist!')
    else:
        context = {
            'user' : user,
        }
        return render(request, 'userm/details.html', context=context)