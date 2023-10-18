from django_hosts import reverse
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext as _

from core.Finances.models import Payment
from core.Utils.Access.decorators import manager_required
from .forms import PaymentFilterForm
from .tables import PaymentTable


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
