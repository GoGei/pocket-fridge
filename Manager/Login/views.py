from django.http import HttpResponseRedirect
from django.conf import settings
from django_hosts import reverse
from django.shortcuts import redirect, render
from django.utils.http import is_safe_url
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import logout, login, authenticate
from .forms import ManagerLoginForm


def login_view(request):
    next_page = request.GET.get('next')
    user = request.user
    if user.is_authenticated:
        if user.is_manager:
            if next_page:
                return HttpResponseRedirect(next_page)
            return redirect(reverse('manager-index', host='manager'))
        else:
            return redirect(reverse('home-index', host='public'))

    initial = {'email': request.COOKIES.get('email', '')}
    form = ManagerLoginForm(request.POST or None, initial=initial)

    if form.is_valid():
        data = form.cleaned_data
        user = authenticate(email=data.get('email'), password=data.get('password'))

        if user:
            if user.is_active and user.is_manager:
                login(request, user)

                remember_me = data.get('remember_me')
                if not remember_me:
                    request.session.set_expiry(0)
                    request.session.modified = True

                if next_page and is_safe_url(next_page, allowed_hosts=settings.ALLOWED_HOSTS):
                    redirect_url = next_page
                else:
                    redirect_url = reverse('manager-index', host='manager')
                response = HttpResponseRedirect(redirect_url)
                response.set_cookie('email', user.email)
                return response

            elif not user.is_manager:
                form.add_error(None, _('User is not manager! You are not allowed to access this page'))
            else:
                form.add_error(None, _('User is not active! Please, contact a manager'))
        else:
            form.add_error(None, _('User with this email and password not found'))

    return render(request, 'Manager/Login/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(reverse('manager-login', host='manager'))
