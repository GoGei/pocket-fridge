from uuid import UUID
from django.shortcuts import get_object_or_404

from core.Utils.Mixins.models import ActiveQuerySet
from core.User.models import User
from core.Fridge.models import Fridge, FridgeProduct
from core.ShoppingList.models import ShoppingList, ShoppingListProduct


def get_fridge_qs(user: User) -> ActiveQuerySet[Fridge]:
    fridge_qs = Fridge.objects.select_related('user', 'fridge_type').active().filter(user=user).order_by('name')
    return fridge_qs


def get_fridge_products(user: User, fridge_id: UUID) -> ActiveQuerySet[FridgeProduct]:
    fridge_qs = get_fridge_qs(user)
    current_fridge = get_object_or_404(fridge_qs, id=fridge_id)
    products = current_fridge.get_products()
    return products


def get_user_products(user: User) -> ActiveQuerySet[FridgeProduct]:
    products = FridgeProduct.objects.select_related('user', 'fridge').active().filter(user=user).order_by('name')
    return products


def get_shopping_list_qs(user: User) -> ActiveQuerySet[ShoppingList]:
    shopping_list_qs = ShoppingList.objects.select_related('user').active().filter(user=user).order_by('name')
    return shopping_list_qs


def get_shopping_list(user: User, shopping_list_id: UUID = None) -> ShoppingList:
    if shopping_list_id:
        shopping_list_qs = get_shopping_list_qs(user)
        shopping_list = get_object_or_404(shopping_list_qs, id=shopping_list_id)
    else:
        shopping_list = ShoppingList.get_shopping_list(user)
    return shopping_list


def get_shopping_list_products(user: User, shopping_list_id: UUID = None) -> ActiveQuerySet[ShoppingListProduct]:
    current_shopping_list = get_shopping_list(user, shopping_list_id)
    products = current_shopping_list.get_products()
    return products


def get_shopping_list_product(user: User, product_id: UUID, shopping_list_id: UUID = None) -> ShoppingListProduct:
    current_shopping_list = get_shopping_list(user, shopping_list_id)
    current_product = get_object_or_404(current_shopping_list.get_products(), id=product_id)
    return current_product
