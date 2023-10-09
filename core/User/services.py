from core.User.models import User
from core.ShoppingList.models import ShoppingList, ShoppingListProduct
from core.Fridge.models import Fridge, FridgeProduct


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
