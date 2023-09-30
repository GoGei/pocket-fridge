from django.shortcuts import render, redirect, get_object_or_404
from django_hosts import reverse

from My import utils, decorators
from .forms import FridgeProductFormAdd, FridgeProductFormEdit


@decorators.my_login_required
def fridge_add(request):
    if '_cancel' in request.POST:
        return redirect(reverse('home-index', host='my'))

    form_body = FridgeProductFormAdd(request.POST or None,
                                     user=request.user)
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
    products = utils.get_fridge_products(request.user, fridge_id)
    return render(request, 'My/Fridge/fridge_view.html',
                  {'fridge_qs': fridge_qs, 'products': products, 'fridge_id': fridge_id})


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
    form_body = FridgeProductFormEdit(request.POST or None,
                                      user=request.user,
                                      instance=product)
    if form_body.is_valid():
        product = form_body.save()
        return redirect(
            reverse('product-view', kwargs={'fridge_id': product.fridge.id, 'product_id': product_id}, host='my'))

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True},
    }
    return render(request, 'My/Fridge/product_edit.html', {'form': form})


@decorators.my_login_required
def product_delete(request, fridge_id, product_id):
    product = get_object_or_404(utils.get_fridge_products(request.user, fridge_id), id=product_id)
    product.get_related_shopping_list_products().update(product=None)
    product.delete()
    return redirect(
        reverse('fridge-view', kwargs={'fridge_id': product.fridge.id}, host='my'))
