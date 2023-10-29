from django.contrib import messages
from django_hosts import reverse
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext as _

from core.Finances.models import Invoice
from core.Finances.tasks import load_invoices_task
from core.Utils.Access.decorators import superuser_required
from .forms import InvoiceFilterForm
from .tables import InvoiceTable
import logging

logger = logging.getLogger(__name__)


@superuser_required
def invoice_list(request):
    qs = Invoice.objects.all().order_by('number')

    filter_form = InvoiceFilterForm(request.GET, queryset=qs, request=request)
    qs = filter_form.qs

    table_body = InvoiceTable(qs, request=request)
    page = request.GET.get("page", 1)
    table_body.paginate(page=page, per_page=settings.ITEMS_PER_PAGE)

    table = {
        'body': table_body,
        'filter': {
            'title': _('Invoices filter'),
            'body': filter_form,
            'action': reverse('manager-stripe-invoice-list', host='manager')
        }
    }
    return render(request, 'Manager/Stripe/Invoice/invoice_list.html',
                  {'table': table})


@superuser_required
def invoice_view(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    return render(request, 'Manager/Stripe/Invoice/invoice_view.html', {'invoice': invoice})


@superuser_required
def invoice_sync(request):
    from ..stripe_integrations.views import stripe_instance_sync
    from core.Finances.stripe.handlers import InvoiceHandler
    return stripe_instance_sync(request,
                                'manager-stripe-invoice',
                                'Manager/Stripe/Invoice/invoice_sync.html',
                                InvoiceHandler)


@superuser_required
def invoice_sync_all(request):
    load_invoices_task.apply_async()
    msg = _('Try to load invoices from stripe')
    messages.info(request, msg)
    logger.info(msg)
    return redirect(reverse('manager-stripe-invoice-list', host='manager'))
