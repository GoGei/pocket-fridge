from django.contrib import messages
from django.contrib.auth import logout
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django_hosts import reverse

from core.ShoppingList.models import ShoppingList
from . import utils
from .forms import FridgeProductFormAdd, FridgeProductFormEdit


@login_required
def home_index(request):
    fridge_qs = utils.get_fridge_qs(request.user)
    # return render(request, 'My/home_index.html', {'fridge_qs': fridge_qs})
    default_fridge = fridge_qs.order_by('name').first()
    return redirect(reverse('fridge-view', kwargs={'fridge_id': default_fridge.id}, host='my'))


@login_required
def profile(request):
    return render(request, 'My/profile.html')


@login_required
def fridge_add(request):
    if '_cancel' in request.POST:
        return redirect(reverse('home-index', host='my'))

    form_body = FridgeProductFormAdd(request.POST or None,
                                     user=request.user)
    if form_body.is_valid():
        product = form_body.save()
        messages.success(request, _(f'Product {product.label} was successfully added'))
        return redirect(reverse('fridge-view', kwargs={'fridge_id': product.fridge_id}, host='my'))

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True},
    }
    return render(request, 'My/fridge_add.html', {'form': form})


@login_required
def fridge_view(request, fridge_id):
    fridge_qs = utils.get_fridge_qs(request.user)
    products = utils.get_fridge_products(request.user, fridge_id)
    return render(request, 'My/fridge_view.html',
                  {'fridge_qs': fridge_qs, 'products': products, 'fridge_id': fridge_id})


@login_required
def product_view(request, fridge_id, product_id):
    products = utils.get_fridge_products(request.user, fridge_id)
    product = get_object_or_404(products, id=product_id)
    return render(request, 'My/product_view.html',
                  {'product': product})


@login_required
def product_edit(request, fridge_id, product_id):
    if '_cancel' in request.POST:
        return redirect(reverse('home-index', host='my'))

    product = get_object_or_404(utils.get_fridge_products(request.user, fridge_id), id=product_id)
    form_body = FridgeProductFormEdit(request.POST or None,
                                      user=request.user,
                                      instance=product)
    if form_body.is_valid():
        product = form_body.save()
        messages.success(request, _(f'Product {product.label} was successfully edited'))
        return redirect(reverse('product-view', kwargs={'fridge_id': product.fridge.id, 'product_id': product_id}, host='my'))

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True},
    }
    return render(request, 'My/product_edit.html', {'form': form})


@login_required
def shopping_list(request):
    shopping_list = ShoppingList.get_shopping_list(request.user)
    products = utils.get_shopping_list_products(request.user, shopping_list.id)
    return render(request, 'My/shopping_list.html',
                  {'shopping_list': shopping_list, 'products': products})


def logout_view(request):
    logout(request)
    return redirect(reverse('login', host='public'))
