from django.test import TestCase

from core.ShoppingList.factories import ShoppingListProductFactory
from ..models import FridgeProduct
from ..factories import FridgeProductFactory


class FridgeProductTests(TestCase):
    def test_create(self):
        obj = FridgeProductFactory.create()
        qs = FridgeProduct.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = FridgeProductFactory.create()
        obj.delete()

        qs = FridgeProduct.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())

    def test_get_products(self):
        fridge_product = FridgeProductFactory.create()
        product = ShoppingListProductFactory.create(product=fridge_product)
        qs = fridge_product.get_related_shopping_list_products()
        self.assertTrue(qs.exists())
        self.assertIn(product, qs)
