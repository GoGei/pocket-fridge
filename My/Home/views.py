from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.conf import settings
from django_hosts import reverse

from My import utils, decorators
from core.Fridge.models import Fridge


@decorators.my_login_required
def home_index(request):
    fridge_qs = utils.get_fridge_qs(request.user)
    # return render(request, 'My/home_index.html', {'fridge_qs': fridge_qs})

    slug = Fridge.DEFAULT_SLUG_TO_DISPLAY
    default_fridge = fridge_qs.filter(fridge_type__slug=slug).first()
    if not default_fridge:
        default_fridge = fridge_qs.order_by('name').first()

    return redirect(reverse('fridge-view', kwargs={'fridge_id': default_fridge.id}, host='my'))


@decorators.my_login_required
def profile(request):
    user_guide_url = settings.USER_GUIDE_URL
    licences_url = settings.LICENCES_URL
    report_error_url = settings.REPORT_ERROR_URL
    return render(request, 'My/profile.html', {
        'user_guide_url': user_guide_url,
        'licences_url': licences_url,
        'report_error_url': report_error_url,
    })


def logout_view(request):
    logout(request)
    return redirect(reverse('login', host='public'))
