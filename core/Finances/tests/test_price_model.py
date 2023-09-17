from django.test import TestCase

from ..models import Price
from ..factories import PriceFactory


class PriceTests(TestCase):
    def test_create(self):
        obj = PriceFactory.create()
        qs = Price.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = PriceFactory.create()
        obj.delete()

        qs = Price.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())
