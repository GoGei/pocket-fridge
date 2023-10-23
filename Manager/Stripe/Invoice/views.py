from django.contrib import messages
from django_hosts import reverse
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext as _

from core.Finances.models import Invoice
from core.Finances.stripe.tasks import load_invoices
from core.Utils.Access.decorators import manager_required
from .forms import InvoiceFilterForm
from .tables import InvoiceTable


@manager_required
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


@manager_required
def invoice_view(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    return render(request, 'Manager/Stripe/Invoice/invoice_view.html', {'invoice': invoice})


@manager_required
def invoice_sync(request):
    from ..stripe_integrations.views import stripe_instance_sync
    from core.Finances.stripe.handlers import InvoiceHandler
    return stripe_instance_sync(request,
                                'manager-stripe-invoice',
                                'Manager/Stripe/Invoice/invoice_sync.html',
                                InvoiceHandler)


@manager_required
def invoice_sync_all(request):
    load_invoices.apply_async()
    messages.info(request, _('Try to load invoices from stripe'))
    return redirect(reverse('manager-stripe-invoice-list', host='manager'))
