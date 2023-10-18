from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django_hosts import reverse
from rest_framework.renderers import JSONRenderer

from My import utils, decorators
from core.Notifications.models import NotificationMessage
from core.User import services
from core.Fridge.models import Fridge
from .forms import ProfileImportForm


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


@decorators.my_login_required
def profile_export(request):
    data = services.get_user_fridge_data(request.user)
    content = JSONRenderer().render(data)

    response = HttpResponse(content, content_type='application/json')
    filename = 'pocket_fridge.json'
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    response['Cache-Control'] = 'no-cache'
    return response


@decorators.my_login_required
def profile_import(request):
    form_body = ProfileImportForm(request.POST or None,
                                  request.FILES or None,
                                  user=request.user)

    if '_cancel' in request.POST:
        return redirect(reverse('profile', host='my'))

    if form_body.is_valid():
        try:
            try:
                form_body.load()
            except ValueError as e:
                form_body.add_error('file', str(e))

            return redirect(reverse('profile', host='my'))
        except ValueError as e:
            form_body.add_error('file', str(e))

    form = {
        'body': form_body,
        'buttons': {'submit': True, 'cancel': True},
        'form_class': 'shopping_list_add_product',
    }

    return render(request, 'My/profile_import.html', {'form': form})


@decorators.my_login_required
def notifications(request):
    notifications_qs = NotificationMessage.objects.filter(recipient=request.user.notify_by_email,
                                                          notification_slug='fridge').order_by('-stamp')
    return render(request, 'My/notifications.html', {'notifications': notifications_qs})


def notifications_remove(request, notification_id):
    NotificationMessage.objects.filter(id=notification_id).delete()
    return redirect(reverse('notifications', host='my'))


def logout_view(request):
    logout(request)
    return redirect(reverse('login', host='public'))
