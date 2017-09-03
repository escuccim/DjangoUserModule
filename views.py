# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .forms import UserForm, UserProfileForm, UserFormWithoutPassword, PasswordForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render,redirect, HttpResponse
from .models import UserProfile

# Create your views here.
def Logout(request):
    logout(request)
    return redirect('blog:index')

def Login(request):
    errors = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return redirect('/')
            else:
                return HttpResponse('Your account is inactive!')
        else:
            errors = 'Your login details are incorrect!'
    else:
        return render(request, 'register/login.html', {'errors': errors})

def Register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.email = user.email

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True

        else:
            return HttpResponse(user_form.errors)
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'register/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def Profile(request):
    user = request.user
    message = None
    errors = False

    try:
        profile = user.userprofile
    except:
        profile = UserProfile()

    if not user.is_authenticated():
        return redirect('register:login')

    if request.method == 'POST':
        user_form = UserFormWithoutPassword(data=request.POST, instance=user)
        profile_form = UserProfileForm(data=request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            message = 'Your profile has been updated!'
        else:
            message = 'Please correct the errors below!'
            errors = True
    else:
        user_form = UserFormWithoutPassword(instance=user)
        profile_form = UserProfileForm(instance=profile)

    return render(request, 'register/profile.html', { 'user_form': user_form, 'profile_form': profile_form, 'user': user, 'message' : message, 'errors': errors})


def ChangePassword(request):
    user = request.user
    message = None
    errors = False

    if not user.is_authenticated():
        return redirect('register:login')

    if request.method == 'POST':
        password_form = PasswordForm(data=request.POST, instance=user)

        if password_form.is_valid():
            old_password = password_form.cleaned_data.get('old_password')

            if not user.check_password(old_password):
                message = 'Your old password is incorrect!'
                errors = True
            else:
                password_form.save()
                message = 'Your password has been updated!'
        else:
            message = 'Please correct the errors below!'
            errors = True

    else:
        password_form = PasswordForm(instance=user)

    return render(request, 'register/changepassword.html', { 'password_form': password_form, 'message' : message, 'errors': errors})