from django.test import TestCase
from Api.v1.tests.base_test_case import ReadOnlyViewSetMixinTestCase
from core.Fridge.factories import FridgeTypeFactory, FridgeFactory, FridgeProductFactory


class FridgeTypeTestCase(ReadOnlyViewSetMixinTestCase, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.base_route = 'fridge-type'
        self.instance = FridgeTypeFactory.create()


class FridgeTestCase(ReadOnlyViewSetMixinTestCase, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.base_route = 'fridge'
        self.instance = FridgeFactory.create(user=self.user)


class FridgeProductTestCase(ReadOnlyViewSetMixinTestCase, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.base_route = 'fridge-products'
        self.fridge = FridgeFactory.create(user=self.user)
        self.instance = FridgeProductFactory.create(user=self.user, fridge=self.fridge)

    def get_list_url(self, action=None, *args, **kwargs):
        action = action or self.APIActions.LIST
        return self.get_reverse(action, (self.fridge.id,), *args, **kwargs)

    def get_detail_url(self, action=None, *args, **kwargs):
        action = action or self.APIActions.DETAIL
        return self.get_reverse(action, (self.fridge.id, self.instance.id,), *args, **kwargs)
