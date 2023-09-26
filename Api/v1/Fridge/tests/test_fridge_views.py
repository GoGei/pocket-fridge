from django.test import TestCase
from django.utils import timezone
from factory import fuzzy

from Api.v1.tests.base_test_case import ReadOnlyViewSetMixinTestCase, ModelViewSetTestCase

from core.Fridge.models import Fridge, FridgeProduct
from core.Fridge.factories import FridgeTypeFactory, FridgeFactory, FridgeProductFactory


class FridgeTypeTestCase(ReadOnlyViewSetMixinTestCase, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.base_route = 'fridge-type'
        self.instance = FridgeTypeFactory.create()


class FridgeTestCase(ModelViewSetTestCase, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.base_route = 'fridge'
        self.instance = FridgeFactory.create(user=self.user)
        self.data = {
            'fridge_type': FridgeTypeFactory.create().id,
            'name': fuzzy.FuzzyText(length=64).fuzz(),
        }
        self.model = Fridge


class FridgeProductTestCase(ModelViewSetTestCase, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.base_route = 'fridge-products'
        self.fridge = FridgeFactory.create(user=self.user)
        self.instance = FridgeProductFactory.create(user=self.user, fridge=self.fridge)
        self.data = {
            'name': fuzzy.FuzzyText(length=64).fuzz(),
            'amount': fuzzy.FuzzyDecimal(1, 100).fuzz(),
            'units': fuzzy.FuzzyChoice(dict(FridgeProduct.FridgeProductUnits.choices).keys()).fuzz(),
            'manufacture_date': fuzzy.FuzzyDate(start_date=timezone.now().date()).fuzz(),
            'shelf_life_date': fuzzy.FuzzyDate(start_date=timezone.now().date()).fuzz(),
            'notes': fuzzy.FuzzyText(length=2048).fuzz(),
        }
        self.model = FridgeProduct

    def get_list_url(self, action=None, *args, **kwargs):
        action = action or self.APIActions.LIST
        return self.get_reverse(action, (self.fridge.id,), *args, **kwargs)

    def get_detail_url(self, action=None, *args, **kwargs):
        action = action or self.APIActions.DETAIL
        return self.get_reverse(action, (self.fridge.id, self.instance.id,), *args, **kwargs)
