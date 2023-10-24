from decimal import Decimal

from django.utils import timezone

from core.User.models import User
from core.ShoppingList.models import ShoppingList, ShoppingListProduct
from core.Fridge.models import Fridge, FridgeProduct, FridgeType


def __shopping_list_product_to_dict(shopping_list_product: ShoppingListProduct) -> dict:
    return {
        'name': shopping_list_product.name,
        'amount': str(shopping_list_product.amount),
        'units': str(shopping_list_product.units),
        'is_checked': shopping_list_product.is_checked,
    }


def __shopping_list_to_dict(shopping_list: ShoppingList) -> dict:
    return {
        'name': shopping_list.name,
        'products': [__shopping_list_product_to_dict(product) for product in shopping_list.get_products()],
    }


def __fridge_product_to_dict(fridge_product: FridgeProduct) -> dict:
    return {
        'name': fridge_product.name,
        'amount': str(fridge_product.amount),
        'units': str(fridge_product.units),
        'notes': fridge_product.notes,
        'barcode': fridge_product.barcode,
    }


def __fridge_to_dict(fridge: Fridge) -> dict:
    return {
        'name': fridge.name,
        'fridge_type_slug': fridge.fridge_type.slug,
        'products': [__fridge_product_to_dict(product) for product in fridge.get_products()]
    }


def get_user_fridge_data(user: User) -> dict:
    user_data = {
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'external_id': user.external_id,
    }

    fridge_qs = Fridge.objects.select_related('user', 'fridge_type').filter(user=user)
    fridge_data = [__fridge_to_dict(fridge) for fridge in fridge_qs]

    shopping_list = ShoppingList.get_shopping_list(user)

    return {
        'user_data': user_data,
        'fridge_data': fridge_data,
        'shopping_list': __shopping_list_to_dict(shopping_list),
    }


def __load_fridge_product(fridge: Fridge, data: dict):
    qs = FridgeProduct.objects.select_related('fridge', 'user').active().filter(fridge=fridge)
    product_name = data.get('name').strip()
    product = qs.filter(name=product_name).first()
    if not product:
        product = FridgeProduct(fridge=fridge, name=product_name, user=fridge.user)

    tomorrow = timezone.now().date() + timezone.timedelta(days=1)

    product.amount = data.get('amount', Decimal(0.0))
    product.units = data.get('units', FridgeProduct.FridgeProductUnits.ITEMS)
    product.notes = data.get('notes', None)
    product.barcode = data.get('barcode', None)
    product.manufacture_date = data.get('manufacture_date', tomorrow)
    product.shelf_life_date = data.get('shelf_life_date', tomorrow)
    product.save()


def __load_fridge(user: User, data: dict):
    fridge_type_slug = data.get('fridge_type_slug')

    qs = Fridge.objects.select_related('user', 'fridge_type').active()
    fridge = qs.filter(user=user, fridge_type__slug=fridge_type_slug).first()

    if not fridge:
        fridge_type = FridgeType.objects.filter(slug=fridge_type_slug).first()
        fridge = Fridge(user=user, fridge_type=fridge_type)

    fridge.name = data['name']
    fridge.save()

    for product_item in data.get('products', []):
        __load_fridge_product(fridge, product_item)


def __load_shopping_list_product(shopping_list: ShoppingList, data: dict):
    product_name = data.get('name').strip()
    product = shopping_list.get_products().filter(name=product_name).first()
    if not product:
        product = ShoppingListProduct(shopping_list=shopping_list, name=product_name)

    product.amount = data.get('amount', Decimal(0.0))
    product.units = data.get('units', FridgeProduct.FridgeProductUnits.ITEMS)
    product.is_checked = data.get('is_checked', False)
    product.save()


def __load_shopping_list(user: User, data: dict):
    shopping_list_name = data.get('name')
    shopping_list = ShoppingList.get_shopping_list(user)

    if not shopping_list:
        shopping_list = ShoppingList(user=user, name=shopping_list_name)
    shopping_list.save()

    for product_item in data.get('products', []):
        __load_shopping_list_product(shopping_list, product_item)


def load_user_fridge_data(user: User, data: dict) -> bool:
    user_data = data['user_data']
    fridge_data = data['fridge_data']
    shopping_list = data['shopping_list']

    user.first_name = user_data['first_name']
    user.last_name = user_data['last_name']
    user.external_id = user_data['external_id']

    for fridge_item in fridge_data:
        __load_fridge(user, fridge_item)

    # for shopping_list_item in shopping_list:
    __load_shopping_list(user, shopping_list)

    return True
