from django.test import TestCase
from core.Fridge.factories import FridgeFactory, FridgeProductFactory
from core.ShoppingList.factories import ShoppingListFactory, ShoppingListProductFactory
from ..factories import UserFactory
from ..services import get_user_fridge_data, load_user_fridge_data


class UserServicesTests(TestCase):
    def test_get_user_fridge_data(self):
        obj = UserFactory.create()

        fridge = FridgeFactory.create(user=obj)
        fridge_product = FridgeProductFactory.create(fridge=fridge, user=obj)
        shopping_list = ShoppingListFactory.create(user=obj)
        shopping_list_product = ShoppingListProductFactory.create(
            shopping_list=shopping_list, user=obj
        )

        data = get_user_fridge_data(obj)
        self.assertTrue(data)
        data = str(data)
        self.assertIn(fridge.fridge_type.slug, data)
        self.assertIn(fridge.name, data)
        self.assertIn(fridge_product.name, data)
        self.assertIn(shopping_list.name, data)
        self.assertIn(shopping_list_product.name, data)

    def test_load_user_data(self):
        obj = UserFactory.create()

        fridge = FridgeFactory.create(user=obj)
        FridgeProductFactory.create(fridge=fridge, user=obj)
        shopping_list = ShoppingListFactory.create(user=obj)
        ShoppingListProductFactory.create(
            shopping_list=shopping_list, user=obj
        )

        data = get_user_fridge_data(obj)

        result = load_user_fridge_data(user=obj, data=data)
        self.assertTrue(result)
