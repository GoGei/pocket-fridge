from django.test import TestCase
from django.utils import timezone

from ..models import PaymentMethod
from ..factories import PaymentMethodFactory


class PaymentMethodTests(TestCase):
    def test_create(self):
        obj = PaymentMethodFactory.create()
        qs = PaymentMethod.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = PaymentMethodFactory.create()
        obj.delete()

        qs = PaymentMethod.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())

    def test_set_as_default(self):
        obj = PaymentMethodFactory.create()
        obj.set_default(user=obj.user)
        self.assertTrue(obj.is_default)

    def test_is_expired(self):
        obj = PaymentMethodFactory.create(expire_date=(timezone.now() - timezone.timedelta(days=50)).date())
        self.assertTrue(obj.is_expired)
