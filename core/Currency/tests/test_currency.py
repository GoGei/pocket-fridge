from django.test import TestCase

from core.Currency.factories import CurrencyFactory
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
