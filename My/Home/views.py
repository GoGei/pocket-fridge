from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.utils.translation import gettext_lazy as _
from django_hosts import reverse
from rest_framework.renderers import JSONRenderer

from My import utils, decorators
from core.Finances.stripe import exceptions
from core.Notifications.models import NotificationMessage
from core.User import services
from core.Fridge.models import Fridge
from core.Licence.models import LicenceVersion, TermsOfUse, PrivacyPolicy
from .forms import ProfileImportForm, ProfileSubscribeForm


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
    licence_version = LicenceVersion.get_default()
    privacy_policy = PrivacyPolicy.get_default(licence_version)
    terms_of_use = TermsOfUse.get_default(licence_version)
    return render(request, 'My/profile.html',
                  {'privacy_policy': privacy_policy, 'terms_of_use': terms_of_use})


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


@decorators.my_login_required
def notifications_remove(request, notification_id):
    NotificationMessage.objects.filter(id=notification_id).delete()
    return redirect(reverse('notifications', host='my'))


@decorators.my_login_required
def profile_subscribe(request):
    form_body = ProfileSubscribeForm(request.POST or None, user=request.user)

    if '_cancel' in request.POST:
        return redirect(reverse('profile', host='my'))

    if form_body.is_valid():
        try:
            form_body.subscribe()
        except exceptions.StripeGetOrCreateException:
            form_body.add_error(None, _('Customer is not created in stripe! Please, contact manager.'))
        except exceptions.StripeObjectCreateException:
            form_body.add_error(None, _('Subscription is not created in stripe! Please, contact manager.'))
        except exceptions.StripeObjectUpdateException:
            form_body.add_error(None,
                                _('Subscription is created in stripe, but not syncronized with our service! Please, contact manager.'))  # noqa
        except ValueError as e:
            form_body.add_error(None, str(e))

        return redirect(reverse('profile', host='my'))

    form = {
        'body': form_body,
        'buttons': {'submit': True, 'cancel': True},
        'form_class': 'shopping_list_add_product',
    }
    return render(request, 'My/profile_subscribe.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(reverse('login', host='public'))
