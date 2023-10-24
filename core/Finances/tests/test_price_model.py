from decimal import Decimal

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

    def test_set_as_default(self):
        obj = PriceFactory.create()
        obj.set_as_default()
        self.assertTrue(obj.is_default)

    def test_stripify_price(self):
        obj = PriceFactory.create(price='1.00')
        self.assertEqual(obj.stripify_price, Decimal('100.00'))
        self.assertEqual(obj.unstripify_price('100'), Decimal('1.00'))

    def test_reccuring(self):
        obj = PriceFactory.create(price='1.00', interval='month')
        self.assertEqual(obj.recurring, {'interval': 'month', 'interval_count': 1, 'usage_type': 'licensed'})
