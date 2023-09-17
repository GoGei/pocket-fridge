from django.test import TestCase

from ..models import Payment
from ..factories import PaymentFactory


class PaymentTests(TestCase):
    def test_create(self):
        obj = PaymentFactory.create()
        qs = Payment.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = PaymentFactory.create()
        obj.delete()

        qs = Payment.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())
