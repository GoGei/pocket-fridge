from django.db.models import When, Case, IntegerField
from django.forms import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django_hosts import reverse

from My import utils, decorators
from .forms import FridgeProductFormAdd, FridgeProductFormEdit


@decorators.my_login_required
def fridge_add(request, fridge_id=None):
    if '_cancel' in request.POST:
        return redirect(reverse('home-index', host='my'))

    if fridge_id:
        fridge = get_object_or_404(utils.get_fridge_qs(request.user), id=fridge_id)
    else:
        fridge = None

    form_body = FridgeProductFormAdd(request.POST or None, request.FILES or None,
                                     user=request.user, fridge=fridge)
    if form_body.is_valid():
        product = form_body.save()
        return redirect(reverse('fridge-view', kwargs={'fridge_id': product.fridge_id}, host='my'))

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True},
        'form_class': 'fridge_add',
    }
    return render(request, 'My/Fridge/fridge_add.html', {'form': form})


@decorators.my_login_required
def fridge_view(request, fridge_id):
    fridge_qs = utils.get_fridge_qs(request.user)
    fridge = get_object_or_404(fridge_qs, id=fridge_id)
    products = utils.get_fridge_products(request.user, fridge_id)
    products = products.annotate_expire_priority().order_by('shelf_life_date', 'name')
    return render(request, 'My/Fridge/fridge_view.html',
                  {'fridge_qs': fridge_qs, 'products': products, 'fridge': fridge})


@decorators.my_login_required
def product_view(request, fridge_id, product_id):
    products = utils.get_fridge_products(request.user, fridge_id)
    product = get_object_or_404(products, id=product_id)
    return render(request, 'My/Fridge/product_view.html',
                  {'product': product})


@decorators.my_login_required
def product_edit(request, fridge_id, product_id):
    if '_cancel' in request.POST:
        return redirect(reverse('home-index', host='my'))

    product = get_object_or_404(utils.get_fridge_products(request.user, fridge_id), id=product_id)
    initial = model_to_dict(product)
    initial['manufacture_date'] = product.manufacture_date.isoformat()
    initial['shelf_life_date'] = product.shelf_life_date.isoformat()

    form_body = FridgeProductFormEdit(request.POST or None, request.FILES or None,
                                      user=request.user,
                                      instance=product, initial=initial)
    if form_body.is_valid():
        product = form_body.save()
        product.notified_as = None
        product.save()
        return redirect(
            reverse('product-view', kwargs={'fridge_id': product.fridge.id, 'product_id': product_id}, host='my'))

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True},
        'form_class': 'product_edit',

    }
    return render(request, 'My/Fridge/product_edit.html', {'form': form})


@decorators.my_login_required
def product_delete(request, fridge_id, product_id):
    product = get_object_or_404(utils.get_fridge_products(request.user, fridge_id), id=product_id)
    product.get_related_shopping_list_products().update(product=None)
    product.delete()
    return redirect(
        reverse('fridge-view', kwargs={'fridge_id': product.fridge.id}, host='my'))
