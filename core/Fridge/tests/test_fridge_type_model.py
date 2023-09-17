from django.test import TestCase

from ..models import FridgeType
from ..factories import FridgeTypeFactory


class FridgeTypeTests(TestCase):
    def test_create(self):
        obj = FridgeTypeFactory.create()
        qs = FridgeType.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = FridgeTypeFactory.create()
        obj.delete()

        qs = FridgeType.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())

    def test_str(self):
        obj = FridgeTypeFactory.create()
        self.assertEqual(str(obj), obj.name)
        self.assertEqual(obj.label, obj.name)
