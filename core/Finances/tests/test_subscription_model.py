from django.test import TestCase

from ..models import Subscription
from ..factories import SubscriptionFactory


class SubscriptionTests(TestCase):
    def test_create(self):
        obj = SubscriptionFactory.create()
        qs = Subscription.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = SubscriptionFactory.create()
        obj.delete()

        qs = Subscription.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())
