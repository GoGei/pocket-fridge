from django_hosts import reverse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _

from core.Finances.models import Price
from core.Utils.Access.decorators import manager_required


@manager_required
def price_view(request, price_id):
    price = get_object_or_404(Price, pk=price_id)
    return render(request, 'Manager/Stripe/Product/Price/price_view.html',
                  {'price': price, 'product_id': price.product.id})


@manager_required
def price_set_as_default(request, price_id):
    price = get_object_or_404(Price, pk=price_id)
    price.set_as_default()
    return redirect(reverse('manager-stripe-price-list', host='manager'))


@manager_required
def price_archive(request, price_id):
    price = get_object_or_404(Price, pk=price_id)
    price.archive()
    return redirect(reverse('manager-stripe-price-list', host='manager'))


@manager_required
def price_sync(request, product_id):
    from core.Finances.stripe import exceptions
    from core.Finances.stripe.handlers import PriceHandler
    from Manager.Stripe.stripe_integrations.forms import StripeSyncForm

    if '_cancel' in request.POST:
        return redirect(reverse('manager-stripe-product-list', args=[product_id], host='manager'))

    form_body = StripeSyncForm(request.POST or None, handler=PriceHandler)

    if form_body.is_valid():
        try:
            instance = form_body.sync()
            messages.success(request, _('Instance "%s" tried to load from stripe') % instance.label)
            return redirect(reverse('manager-stripe-product-price-view', args=[instance.id], host='manager'))
        except exceptions.StripeException as e:
            messages.error(request, e)
            return redirect(reverse('manager-stripe-product-list', args=[product_id], host='manager'))

    form = {'body': form_body,
            'title': _('Load from stripe'),
            'buttons': {'save': True, 'cancel': True}}
    return render(request,
                  'Manager/Stripe/Product/Price/price_sync.html',
                  {'form': form, 'product_id': product_id})
