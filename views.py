# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .forms import UserForm, UserProfileForm, UserFormWithoutPassword, PasswordForm, PasswordResetForm, ChangePasswordForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render,redirect, HttpResponse
from .models import UserProfile
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.template import loader
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

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
                return HttpResponse(_('Your account is inactive!'))
        else:
            errors = _('Your login details are incorrect!')
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
            profile = profile_form.save(commit=False)
            profile.user = user
            message = _('Your profile has been updated!')
        else:
            message = _('Please correct the errors below!')
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
                message = _('Your old password is incorrect!')
                errors = True
            else:
                password_form.save()
                message = _('Your password has been updated!')
        else:
            message = _('Please correct the errors below!')
            errors = True

    else:
        password_form = PasswordForm(instance=user)

    return render(request, 'register/changepassword.html', { 'password_form': password_form, 'message' : message, 'errors': errors})


def RequestPasswordReset(request):
    user = request.user
    errors = None

    if user.is_authenticated():
        return redirect('register:changepassword')

    if request.method == 'POST':
        password_reset_form = PasswordResetForm(data=request.POST)

        if password_reset_form.is_valid():
            user = User.objects.filter(email=password_reset_form.cleaned_data.get("email"))[0]
            if user:
                # if the user is valid create a reset token
                profile = user.userprofile
                profile.password_token = get_random_string(length=20)
                profile.save()

                # then email it to the user with a link
                html_message = loader.render_to_string('register/password_reset_email_template.html', { 'profile' : profile })

                send_mail('Your password reset', html_message, profile.user.email, [settings.DEFAULT_FROM_EMAIL],fail_silently=False, html_message=html_message)

            else:
                errors = _('This email does not match our system!')

    else:
        password_reset_form = PasswordResetForm()

    return render(request, 'register/request_passwordreset.html', {'password_reset_form': password_reset_form, 'errors': errors})


def ResetPassword(request, id, token):
    user = User.objects.get(pk=id)
    errors = None
    message = None

    if user.userprofile.password_token != token:
        errors = _('This password reset link is not valid!')

    if request.method == 'POST':
        password_form = ChangePasswordForm(data=request.POST)

        if password_form.is_valid():
            # update the password
            user.set_password(password_form.cleaned_data.get('password'))
            user.save()

            # erase the token
            user.userprofile.password_token = ''
            user.userprofile.save()

            # return a success message
            message = _("Your password has been successfully updated!")

            return redirect('register:login')
        else:
            errors = _("Please correct the errors below!")

    else:
        password_form = ChangePasswordForm(instance=user)

    return render(request, 'register/reset_password_form.html', { 'password_form': password_form, 'errors' : errors, 'message' : message, 'user': user, 'token' : token })