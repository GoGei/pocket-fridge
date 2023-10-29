from django_hosts import reverse
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext as _

from core.Finances.models import Product, Price
from core.Utils.Access.decorators import superuser_required
from .forms import ProductFilterForm
from .tables import ProductTable
from .Price.forms import PriceFilterForm
from .Price.tables import PriceTable
import logging

logger = logging.getLogger(__name__)


@superuser_required
def product_list(request):
    qs = Product.objects.all().order_by('-is_default', '-name')

    filter_form = ProductFilterForm(request.GET, queryset=qs, request=request)
    qs = filter_form.qs

    table_body = ProductTable(qs, request=request)
    page = request.GET.get("page", 1)
    table_body.paginate(page=page, per_page=settings.ITEMS_PER_PAGE)

    table = {
        'body': table_body,
        'filter': {
            'title': _('Products filter'),
            'body': filter_form,
            'action': reverse('manager-stripe-product-list', host='manager')
        }
    }
    return render(request, 'Manager/Stripe/Product/product_list.html',
                  {'table': table})


@superuser_required
def product_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    qs = Price.objects.select_related('product').filter(product=product).order_by('-is_default')

    filter_form = PriceFilterForm(request.GET, queryset=qs, request=request)
    qs = filter_form.qs

    table_body = PriceTable(qs, request=request)
    page = request.GET.get("page", 1)
    table_body.paginate(page=page, per_page=settings.ITEMS_PER_PAGE)

    table = {
        'body': table_body,
        'filter': {
            'title': _('Prices filter'),
            'body': filter_form,
            'action': reverse('manager-stripe-product-view', args=[product_id], host='manager')
        },
        'skips': {'table_no_data': True}
    }
    return render(request, 'Manager/Stripe/Product/product_view.html',
                  {'product': product, 'table': table})


@superuser_required
def product_set_as_default(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    msg = _(f'Product {product.label} was successfully set as default')
    product.set_as_default()
    logger.info(msg)
    return redirect(reverse('manager-stripe-product-list', host='manager'))


@superuser_required
def product_archive(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    msg = _(f'Product {product.label} was successfully archived')
    product.archive()
    logger.info(msg)
    return redirect(reverse('manager-stripe-product-list', host='manager'))


@superuser_required
def product_sync(request):
    from ..stripe_integrations.views import stripe_instance_sync
    from core.Finances.stripe.handlers import ProductHandler
    return stripe_instance_sync(request,
                                'manager-stripe-product',
                                'Manager/Stripe/Product/product_sync.html',
                                ProductHandler)
