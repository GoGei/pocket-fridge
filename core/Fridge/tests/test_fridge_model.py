from django.test import TestCase

from ..models import Fridge
from ..factories import FridgeFactory


class FridgeTests(TestCase):
    def test_create(self):
        obj = FridgeFactory.create()
        qs = Fridge.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = FridgeFactory.create()
        obj.delete()

        qs = Fridge.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())
