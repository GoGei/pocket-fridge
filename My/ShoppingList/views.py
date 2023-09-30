from django.shortcuts import render, redirect
from django_hosts import reverse

from My import utils, decorators
from .forms import ShoppingListProductFormAdd, ShoppingListProductFormEdit


@decorators.my_login_required
def shopping_list_view(request):
    shopping_list = utils.get_shopping_list(request.user)
    products = utils.get_shopping_list_products(request.user, shopping_list.id)
    return render(request, 'My/ShoppingList/shopping_list.html',
                  {'shopping_list': shopping_list, 'products': products})


@decorators.my_login_required
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
        'form_class': 'shopping_list_add_product',
    }
    return render(request, 'My/ShoppingList/shopping_list_product_add.html', {'form': form})


@decorators.my_login_required
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
    return render(request, 'My/ShoppingList/shopping_list_product_edit.html', {'form': form})


@decorators.my_login_required
def shopping_list_check_product(request, product_id):
    product = utils.get_shopping_list_product(request.user, product_id=product_id)
    product.check_product()
    return redirect(reverse('shopping-list', host='my'))


@decorators.my_login_required
def shopping_list_uncheck_product(request, product_id):
    product = utils.get_shopping_list_product(request.user, product_id=product_id)
    product.uncheck_product()
    return redirect(reverse('shopping-list', host='my'))


@decorators.my_login_required
def shopping_list_delete_product(request, product_id):
    product = utils.get_shopping_list_product(request.user, product_id=product_id)
    product.delete()
    return redirect(reverse('shopping-list', host='my'))
