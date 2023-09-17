from django.test import TestCase

from ..models import ShoppingList
from ..factories import ShoppingListFactory


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
