from django.test import TestCase
from factory import fuzzy
from rest_framework import status

from Api.v1.tests.base_test_case import ModelViewSetTestCase, ReadOnlyViewSetMixinTestCase
from core.Fridge.factories import FridgeProductFactory
from core.Fridge.models import FridgeProduct

from core.ShoppingList.models import ShoppingListProduct
from core.ShoppingList.factories import ShoppingListFactory, ShoppingListProductFactory


class ShoppingListTestCase(ReadOnlyViewSetMixinTestCase, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.base_route = 'shopping-list'
        self.instance = ShoppingListFactory.create(user=self.user)


class ShoppingListProductTestCase(ModelViewSetTestCase, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.base_route = 'shopping-list-products'
        self.shopping_list = ShoppingListFactory.create(user=self.user)
        self.instance = ShoppingListProductFactory.create(user=self.user, shopping_list=self.shopping_list)
        self.data = {
            'name': fuzzy.FuzzyText(length=64).fuzz(),
            'amount': fuzzy.FuzzyDecimal(1, 100).fuzz(),
            'units': fuzzy.FuzzyChoice(dict(FridgeProduct.FridgeProductUnits.choices).keys()).fuzz(),
        }
        self.model = ShoppingListProduct

    def get_list_url(self, action=None, *args, **kwargs):
        action = action or self.APIActions.LIST
        return self.get_reverse(action, (self.shopping_list.id,), *args, **kwargs)

    def get_detail_url(self, action=None, *args, **kwargs):
        action = action or self.APIActions.DETAIL
        return self.get_reverse(action, (self.shopping_list.id, self.instance.id,), *args, **kwargs)

    def test_create_from_product(self):
        prev_counter = self.model.objects.all().count()

        data = {
            'product': FridgeProductFactory.create(user=self.user).id
        }
        response = self.client.post(self.get_list_url(action='create-from-product'), data=data, HTTP_HOST='api',
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.check_key_equality(response.data, data)

        new_counter = self.model.objects.all().count()
        self.assertEqual(new_counter, prev_counter + 1)
