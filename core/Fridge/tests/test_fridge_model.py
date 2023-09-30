from django.test import TestCase

from ..models import Fridge
from ..factories import FridgeFactory, FridgeTypeFactory, FridgeProductFactory
from ...User.factories import UserFactory


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

    def test_create_fridges_for_user(self):
        to_create = FridgeTypeFactory.create(create_on_user_creation=True)
        not_to_create = FridgeTypeFactory.create(create_on_user_creation=False)

        user = UserFactory.create()
        instances = Fridge.create_fridges_for_user(user)
        names = instances.values_list('name', flat=True)
        self.assertIn(to_create.name, names)
        self.assertNotIn(not_to_create.name, names)

        self.assertRaises(ValueError, Fridge.create_fridges_for_user, user=user)

    def test_get_products(self):
        fridge = FridgeFactory.create()
        fridge_product = FridgeProductFactory.create(fridge=fridge)
        qs = fridge.get_products()
        self.assertTrue(qs.exists())
        self.assertIn(fridge_product, qs)
