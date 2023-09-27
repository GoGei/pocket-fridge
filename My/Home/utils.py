from uuid import UUID
from django.shortcuts import get_object_or_404

from core.User.models import User
from core.Fridge.models import Fridge
from core.ShoppingList.models import ShoppingList


def get_fridge_qs(user: User):
    fridge_qs = Fridge.objects.select_related('user', 'fridge_type').active().filter(user=user).order_by('name')
    return fridge_qs


def get_fridge_products(user: User, fridge_id: UUID):
    fridge_qs = get_fridge_qs(user)
    current_fridge = get_object_or_404(fridge_qs, id=fridge_id)
    products = current_fridge.get_products()
    return products


def get_shopping_list(user: User):
    shopping_list_qs = ShoppingList.objects.select_related('user').active().filter(user=user).order_by('name')
    return shopping_list_qs


def get_shopping_list_products(user: User, shopping_list_id: UUID):
    shopping_list_qs = ShoppingList.objects.select_related('user').active().filter(user=user).order_by('name')
    current_shopping_list = get_object_or_404(shopping_list_qs, id=shopping_list_id)
    products = current_shopping_list.get_products()
    return products
