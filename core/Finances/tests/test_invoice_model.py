from django.test import TestCase

from ..models import Invoice
from ..factories import InvoiceFactory


class InvoiceTests(TestCase):
    def test_create(self):
        obj = InvoiceFactory.create()
        qs = Invoice.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = InvoiceFactory.create()
        obj.delete()

        qs = Invoice.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())
