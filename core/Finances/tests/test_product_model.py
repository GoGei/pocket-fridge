from django.test import TestCase

from ..models import Product
from ..factories import ProductFactory


class ProductTests(TestCase):
    def test_create(self):
        obj = ProductFactory.create()
        qs = Product.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = ProductFactory.create()
        obj.delete()

        qs = Product.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())

    def test_set_as_default(self):
        obj = ProductFactory.create()
        obj.set_as_default()
        self.assertTrue(obj.is_default)
