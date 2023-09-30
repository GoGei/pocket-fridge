from django.test import TestCase

from core.User.factories import UserFactory
from ..models import ShoppingList
from ..factories import ShoppingListFactory, ShoppingListProductFactory


class ShoppingListTests(TestCase):
    def test_create(self):
        obj = ShoppingListFactory.create()
        qs = ShoppingList.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = ShoppingListFactory.create()
        obj.delete()

        qs = ShoppingList.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())

    def test_get_products(self):
        obj = ShoppingListProductFactory.create()
        qs = obj.shopping_list.get_products()
        self.assertTrue(qs.exists())
        self.assertIn(obj, qs)

    def test_create_shopping_list_for_user(self):
        user = UserFactory.create()
        instance = ShoppingList.create_shopping_list_for_user(user)
        self.assertRaises(ValueError, ShoppingList.create_shopping_list_for_user, user)
        self.assertEqual(instance.user, user)
        self.assertEqual(instance, ShoppingList.get_shopping_list(user))
