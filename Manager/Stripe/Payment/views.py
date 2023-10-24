from django.contrib import messages
from django_hosts import reverse
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext as _

from core.Finances.models import Payment
from core.Finances.tasks import load_payments_task
from core.Utils.Access.decorators import manager_required
from .forms import PaymentFilterForm
from .tables import PaymentTable
import logging

logger = logging.getLogger(__name__)


@manager_required
def payment_list(request):
    qs = Payment.objects.all().order_by('-created_stamp')

    filter_form = PaymentFilterForm(request.GET, queryset=qs, request=request)
    qs = filter_form.qs

    table_body = PaymentTable(qs, request=request)
    page = request.GET.get("page", 1)
    table_body.paginate(page=page, per_page=settings.ITEMS_PER_PAGE)

    table = {
        'body': table_body,
        'filter': {
            'title': _('Payments filter'),
            'body': filter_form,
            'action': reverse('manager-stripe-payment-list', host='manager')
        }
    }
    return render(request, 'Manager/Stripe/Payment/payment_list.html',
                  {'table': table})


@manager_required
def payment_view(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)
    return render(request, 'Manager/Stripe/Payment/payment_view.html', {'payment': payment})


@manager_required
def payment_sync(request):
    from ..stripe_integrations.views import stripe_instance_sync
    from core.Finances.stripe.handlers import PaymentHandler
    return stripe_instance_sync(request,
                                'manager-stripe-payment',
                                'Manager/Stripe/Payment/payment_sync.html',
                                PaymentHandler)


@manager_required
def payment_sync_all(request):
    load_payments_task.apply_async()
    msg = _('Try to load payments from stripe')
    messages.info(request, msg)
    logger.info(msg)
    return redirect(reverse('manager-stripe-payment-list', host='manager'))
