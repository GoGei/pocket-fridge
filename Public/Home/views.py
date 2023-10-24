from django_hosts import reverse
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils.http import is_safe_url
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import logout, login, authenticate

from core.Finances.models import Price
from core.User.models import User
from .forms import UserRegistrationForm, UserLoginForm, UserForgotPasswordForm, UserResetPasswordForm
from core.Licence.models import LicenceVersion, TermsOfUse, PrivacyPolicy


def home_index(request):
    # return redirect(reverse('login', host='public'))
    prices = Price.objects.active().integrated().order_by('price')
    return render(request, 'Public/home_index.html', {'prices': prices})


def register(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        user.sign_licence()
        user.send_registration_email()
        return redirect(reverse('register-success', host='public'))

    licence_version = LicenceVersion.get_default()
    privacy_policy = PrivacyPolicy.get_default(licence_version)
    terms_of_use = TermsOfUse.get_default(licence_version)
    return render(request, 'Public/auth/auth-register.html',
                  {'form': form,
                   'privacy_policy': privacy_policy,
                   'terms_of_use': terms_of_use,
                   })


def register_success(request):
    return render(request, 'Public/auth/auth-register-success.html')


def register_activate(request, key):
    user = User.get_by_registration_key(key)

    if not user:
        messages.warning(request, _('For this key user not found'))
        User.clear_registration_keys(key)
        return redirect(reverse('home-index', host='public'))

    user.activate()
    User.clear_forgot_password_keys(key)
    login(request, user)
    return redirect(reverse('home-index', host='public'))


def login_view(request):
    next_page = request.GET.get('next')
    user = request.user
    if user.is_authenticated:
        if next_page:
            return HttpResponseRedirect(next_page)
        return redirect(reverse('home-index', host='my'))

    initial = {'email': request.COOKIES.get('email', '')}
    form = UserLoginForm(request.POST or None, initial=initial)

    if form.is_valid():
        data = form.cleaned_data
        user = authenticate(email=data.get('email'), password=data.get('password'))

        if user:
            if user.is_active:
                login(request, user)

                remember_me = data.get('remember_me')
                if not remember_me:
                    request.session.set_expiry(0)
                    request.session.modified = True

                if next_page and is_safe_url(next_page, allowed_hosts=settings.ALLOWED_HOSTS):
                    redirect_url = next_page
                else:
                    redirect_url = reverse('home-index', host='my')
                response = HttpResponseRedirect(redirect_url)
                response.set_cookie('email', user.email)
                return response
            else:
                form.add_error(None, _('User is not active! Please, contact a manager'))
        else:
            form.add_error(None, _('User with this email and password not found'))

    return render(request, 'Public/auth/auth-login-basic.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(reverse('login', host='public'))


def forgot_password(request):
    form = UserForgotPasswordForm(request.POST or None)
    if form.is_valid():
        user = form.cleaned_data.get('user')
        user.send_forgot_password_email()
        return redirect(reverse('forgot-password-success', host='public'))
    return render(request, 'Public/auth/auth-forgot-password.html', {'form': form})


def forgot_password_success(request):
    return render(request, 'Public/auth/auth-forgot-password-success.html')


def forgot_password_reset(request, key):
    user = User.get_by_forgot_password_key(key)
    if not user:
        messages.warning(request, _('For this key user not found'))
        User.clear_forgot_password_keys(key)
        return redirect(reverse('home-index', host='public'))

    form = UserResetPasswordForm(request.POST or None)
    if form.is_valid():
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        User.clear_forgot_password_keys(key)
        login(request, user)
        return redirect(reverse('home-index', host='my'))

    return render(request, 'Public/auth/auth-forgot-password-reset.html', {'form': form})


def licences(request):
    version = LicenceVersion.get_default()
    privacy_policy = PrivacyPolicy.get_default(version)
    terms_of_use = TermsOfUse.get_default(version)
    return render(request, 'Public/licences.html', {
        'version': version,
        'privacy_policy': privacy_policy,
        'terms_of_use': terms_of_use
    })


def go_to_fridge_view(request):
    return redirect(reverse('home-index', host='my'))
