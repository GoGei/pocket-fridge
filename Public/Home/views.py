from django.shortcuts import render, redirect
from django_hosts import reverse

from .forms import UserRegistrationForm
from core.Licence.models import LicenceVersion, TermsOfUse, PrivacyPolicy


def home_index(request):
    return render(request, 'Public/home_index.html')


def register(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        user.send_registration_email()
        return redirect(reverse('register-success', host='public'))
    return render(request, 'Public/auth-register-basic.html', {'form': form})


def register_success(request):
    return render(request, 'Public/auth-register-success.html')


def login(request):
    return render(request, 'Public/auth-login-basic.html')


def forgot_password(request):
    return render(request, 'Public/auth-forgot-password-basic.html')


def licences(request):
    version = LicenceVersion.get_default()
    privacy_policy = PrivacyPolicy.get_default(version)
    terms_of_use = TermsOfUse.get_default(version)
    return render(request, 'Public/licences.html', {
        'version': version,
        'privacy_policy': privacy_policy,
        'terms_of_use': terms_of_use
    })
