from django.test import TestCase

from core.Currency.factories import CurrencyFactory, CurrencyDefaultFactory
from core.Currency.models import Currency


class CurrencyTests(TestCase):
    def test_create(self):
        obj = CurrencyFactory.create()
        qs = Currency.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = CurrencyFactory.create()
        obj.delete()

        qs = Currency.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())

    def test_get_default(self):
        obj = CurrencyDefaultFactory.create()
        default = Currency.objects.get_default()
        self.assertEqual(obj, default)
