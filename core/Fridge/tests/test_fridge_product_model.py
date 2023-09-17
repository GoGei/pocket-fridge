from django.test import TestCase

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
