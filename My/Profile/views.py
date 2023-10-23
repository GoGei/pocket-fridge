from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django_hosts import reverse
from rest_framework.renderers import JSONRenderer

from My import decorators
from core.User import services
from core.Finances.stripe import exceptions
from core.Finances.stripe.handlers import CustomerHandler, SubscriptionHandler
from core.Licence.models import LicenceVersion, TermsOfUse, PrivacyPolicy
from .forms import ProfileImportForm, ProfileSubscribeForm, ProfilePaymentMethodForm


@decorators.my_login_required
def profile(request):
    licence_version = LicenceVersion.get_default()
    privacy_policy = PrivacyPolicy.get_default(licence_version)
    terms_of_use = TermsOfUse.get_default(licence_version)
    subscription = request.user.get_subscription()
    return render(request, 'My/Profile/profile.html',
                  {'privacy_policy': privacy_policy, 'terms_of_use': terms_of_use, 'subscription': subscription})


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
        'form_class': 'profile_import',
    }

    return render(request, 'My/Profile/profile_import.html', {'form': form})


@decorators.my_login_required
def profile_subscribe(request):
    user = request.user
    payment_method = user.get_payment_method()
    if not payment_method or payment_method and payment_method.is_expired:
        return redirect(reverse('profile-add-payment-method', host='my'))

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
        'form_class': 'profile_subscribe',
    }
    return render(request, 'My/Profile/profile_subscribe.html',
                  {'form': form, 'payment_method': payment_method})


@decorators.my_login_required
def profile_add_payment_method(request):
    form_body = ProfilePaymentMethodForm(request.POST or None,
                                         user=request.user)

    if '_cancel' in request.POST:
        return redirect(reverse('profile', host='my'))

    if not request.user.external_id:
        try:
            CustomerHandler().get_or_create(request.user)
            return redirect(reverse('profile', host='my'))
        except exceptions.StripeGetOrCreateException:
            form_body.add_error(None, _('Customer is not created in stripe! Please, contact manager.'))

    if form_body.is_valid():
        try:
            form_body.save()
            return redirect(reverse('profile-subscribe', host='my'))
        except exceptions.StripePaymentMethodCreateException as e:
            form_body.add_error(None, _('Card can not be created in stripe! Please, contact manager.'))
        except exceptions.StripePaymentMethodDataInvalidException as e:
            form_body.add_error(None, _('Card data is invalid! Please, contact manager.'))
        except exceptions.StripePaymentMethodAttachError as e:
            form_body.add_error(None, _('Can not attach card to customer! Please, contact manager.'))
        except exceptions.StripeUnhandledException as e:
            form_body.add_error(None, _('Some error occurred! Please, contact manager.'))

    form = {
        'body': form_body,
        'buttons': {'submit': True, 'cancel': True},
        'form_class': 'add_card',
    }

    return render(request, 'My/Profile/profile_add_payment_method.html', {'form': form})


@decorators.my_login_required
def profile_cancel_subscription(request):
    user = request.user
    subscription = user.get_subscription()
    if not subscription:
        return redirect(reverse('profile', host='my'))

    try:
        subscription.archive(request.user)
        SubscriptionHandler().destroy(subscription)
    except (exceptions.StripeObjectCannotDeleteException, exceptions.StripeUnhandledException) as e:
        print(str(e))

    return redirect(reverse('profile', host='my'))
