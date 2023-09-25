from django_hosts import reverse
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils.http import is_safe_url
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import logout, login, authenticate

from .forms import UserRegistrationForm, UserLoginForm
from core.Licence.models import LicenceVersion, TermsOfUse, PrivacyPolicy


def home_index(request):
    return render(request, 'Public/home_index.html')


def register(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        user.send_registration_email()
        return redirect(reverse('register-success', host='public'))
    return render(request, 'Public/auth/auth-register.html', {'form': form})


def register_success(request):
    return render(request, 'Public/auth/auth-register-success.html')


def login_view(request):
    next_page = request.GET.get('next')
    user = request.user
    if user.is_authenticated:
        if next_page:
            return HttpResponseRedirect(next_page)
        return redirect(reverse('home-index', host='public'))

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
                    redirect_url = reverse('home-index', host='public')
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
    return render(request, 'Public/auth/auth-forgot-password-basic.html')


def licences(request):
    version = LicenceVersion.get_default()
    privacy_policy = PrivacyPolicy.get_default(version)
    terms_of_use = TermsOfUse.get_default(version)
    return render(request, 'Public/licences.html', {
        'version': version,
        'privacy_policy': privacy_policy,
        'terms_of_use': terms_of_use
    })
