from django_hosts import reverse
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext as _

from core.Finances.models import Product
from core.Utils.Access.decorators import manager_required
from .forms import ProductFilterForm
from .tables import ProductTable


@manager_required
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


@manager_required
def product_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'Manager/Stripe/Product/product_view.html', {'product': product})


@manager_required
def product_set_as_default(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.set_as_default()
    return redirect(reverse('manager-stripe-product-list', host='manager'))


@manager_required
def product_archive(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.archive()
    return redirect(reverse('manager-stripe-product-list', host='manager'))
