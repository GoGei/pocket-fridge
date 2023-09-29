from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django_hosts import reverse

from . import utils
from .forms import FridgeProductFormAdd, FridgeProductFormEdit, ShoppingListProductFormAdd, ShoppingListProductFormEdit


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
        return redirect(
            reverse('product-view', kwargs={'fridge_id': product.fridge.id, 'product_id': product_id}, host='my'))

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True},
    }
    return render(request, 'My/product_edit.html', {'form': form})


@login_required
def product_delete(request, fridge_id, product_id):
    product = get_object_or_404(utils.get_fridge_products(request.user, fridge_id), id=product_id)
    product.get_related_shopping_list_products().update(product=None)
    product.delete()
    return redirect(
        reverse('fridge-view', kwargs={'fridge_id': product.fridge.id}, host='my'))


@login_required
def shopping_list_view(request):
    shopping_list = utils.get_shopping_list(request.user)
    products = utils.get_shopping_list_products(request.user, shopping_list.id)
    return render(request, 'My/shopping_list.html',
                  {'shopping_list': shopping_list, 'products': products})


@login_required
def shopping_list_add_product(request):
    if '_cancel' in request.POST:
        return redirect(reverse('shopping-list', host='my'))

    form_body = ShoppingListProductFormAdd(request.POST or None,
                                           user=request.user)
    if form_body.is_valid():
        form_body.save()
        return redirect(reverse('shopping-list', host='my'))

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True},
    }
    return render(request, 'My/shopping_list_product_add.html', {'form': form})


@login_required
def shopping_list_edit_product(request, product_id):
    if '_cancel' in request.POST:
        return redirect(reverse('shopping-list', host='my'))

    user = request.user
    product = utils.get_shopping_list_product(user, product_id=product_id)
    form_body = ShoppingListProductFormEdit(request.POST or None,
                                            user=user,
                                            instance=product)
    if form_body.is_valid():
        form_body.save()
        return redirect(reverse('shopping-list', host='my'))

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True},
    }
    return render(request, 'My/shopping_list_product_edit.html', {'form': form})


@login_required
def shopping_list_check_product(request, product_id):
    product = utils.get_shopping_list_product(request.user, product_id=product_id)
    product.check_product()
    return redirect(reverse('shopping-list', host='my'))


@login_required
def shopping_list_uncheck_product(request, product_id):
    product = utils.get_shopping_list_product(request.user, product_id=product_id)
    product.uncheck_product()
    return redirect(reverse('shopping-list', host='my'))


@login_required
def shopping_list_delete_product(request, product_id):
    product = utils.get_shopping_list_product(request.user, product_id=product_id)
    product.delete()
    return redirect(reverse('shopping-list', host='my'))


def logout_view(request):
    logout(request)
    return redirect(reverse('login', host='public'))


@login_required
def test_view(request):
    return render(request, 'My/test_test.html')
