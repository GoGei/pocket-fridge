from django.test import TestCase

from ..models import ShoppingListProduct
from ..factories import ShoppingListProductFactory


class ShoppingListProductTests(TestCase):
    def test_create(self):
        obj = ShoppingListProductFactory.create()
        qs = ShoppingListProduct.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = ShoppingListProductFactory.create()
        obj.delete()

        qs = ShoppingListProduct.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())
