from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import ugettext_lazy as _
from django_hosts import reverse

from core.Finances.stripe import exceptions
from Manager.Stripe.stripe_integrations.forms import StripeSyncForm
import logging

logger = logging.getLogger(__name__)


def stripe_instance_sync(request, base_url, template, handler, context=None):
    if '_cancel' in request.POST:
        return redirect(reverse(f'{base_url}-list', host='manager'))

    form_body = StripeSyncForm(request.POST or None, handler=handler)

    if form_body.is_valid():
        try:
            instance = form_body.sync()
            msg = _('Instance "%s" tried to load from stripe') % instance.label
            messages.success(request, msg)
            logger.info(msg)
            return redirect(reverse(f'{base_url}-view', args=[instance.id], host='manager'))
        except exceptions.StripeException as e:
            msg = str(e)
            messages.error(request, msg)
            logger.info(msg)
            return redirect(reverse(f'{base_url}-list', host='manager'))

    form = {'body': form_body,
            'title': _('Load from stripe'),
            'buttons': {'save': True, 'cancel': True}}
    ctx = {'form': form}
    ctx.update(context or {})
    return render(request,
                  template,
                  ctx)
