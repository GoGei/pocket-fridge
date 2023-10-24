from django.utils import timezone
from factory import fuzzy
from django.test import Client, TestCase
from django_hosts.resolvers import reverse

from core.Fridge.factories import FridgeProductFactory
from core.Fridge.models import FridgeProduct
from core.User.factories import UserFactory
from core.ShoppingList.models import ShoppingListProduct, ShoppingList
from core.ShoppingList.factories import ShoppingListFactory, ShoppingListProductFactory


class ShoppingListViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.client = Client()
        self.client.force_login(self.user)
        self.user.activate()
        self.shopping_list = ShoppingList.get_shopping_list(self.user)

    def test_shopping_list_view(self):
        shopping_list = self.shopping_list
        product = ShoppingListProductFactory.create(shopping_list=shopping_list)
        response = self.client.get(reverse('shopping-list', host='my'),
                                   HTTP_HOST='my')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, shopping_list.id)
        self.assertContains(response, product.id)

    def test_product_add_get(self):
        ShoppingListFactory.create(user=self.user)
        response = self.client.get(reverse('shopping-list-add-product',
                                           host='my'),
                                   HTTP_HOST='my', data={'_cancel': True})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'My/ShoppingList/shopping_list_product_add.html')

    def test_product_edit_get(self):
        shopping_list = ShoppingListFactory.create(user=self.user)
        product = ShoppingListProductFactory.create(shopping_list=shopping_list, name='test')

        response = self.client.get(reverse('shopping-list-edit-product',
                                           kwargs={'product_id': product.id},
                                           host='my'),
                                   HTTP_HOST='my', data={'_cancel': True})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'My/ShoppingList/shopping_list_product_edit.html')

    def test_product_add_cancel(self):
        ShoppingListFactory.create(user=self.user)
        response = self.client.post(reverse('shopping-list-add-product',
                                            host='my'),
                                    HTTP_HOST='my', data={'_cancel': True})
        self.assertEqual(response.status_code, 302)

    def test_product_add_success(self):
        shopping_list = ShoppingListFactory.create(user=self.user)

        data = {
            'name': fuzzy.FuzzyText(length=64).fuzz(),
            'shopping_list': shopping_list.id,
            'amount': fuzzy.FuzzyDecimal(low=1, high=100).fuzz(),
            'units': fuzzy.FuzzyChoice(dict(FridgeProduct.FridgeProductUnits.choices).keys()).fuzz(),
            'manufacture_date': fuzzy.FuzzyDate(start_date=timezone.now().date()).fuzz(),
            'shelf_life_date': fuzzy.FuzzyDate(start_date=timezone.now().date()).fuzz(),
            'notes': fuzzy.FuzzyText(length=2048).fuzz(),
        }
        response = self.client.post(reverse('shopping-list-add-product',
                                            host='my'),
                                    HTTP_HOST='my', data=data)
        self.assertEqual(response.status_code, 302)

    def test_product_edit(self):
        shopping_list = ShoppingListFactory.create(user=self.user)
        product = ShoppingListProductFactory.create(shopping_list=shopping_list)
        response = self.client.post(reverse('shopping-list-edit-product',
                                            kwargs={'product_id': product.id},
                                            host='my'),
                                    HTTP_HOST='my', data={'_cancel': True})
        self.assertEqual(response.status_code, 302)

    def test_product_edit_success(self):
        shopping_list = ShoppingListFactory.create(user=self.user)
        product = ShoppingListProductFactory.create(shopping_list=shopping_list, name='test')

        data = {
            'name': fuzzy.FuzzyText(length=64).fuzz(),
            'shopping_list': shopping_list.id,
            'amount': fuzzy.FuzzyDecimal(low=1, high=100).fuzz(),
            'units': fuzzy.FuzzyChoice(dict(FridgeProduct.FridgeProductUnits.choices).keys()).fuzz(),
            'manufacture_date': fuzzy.FuzzyDate(start_date=timezone.now().date()).fuzz(),
            'shelf_life_date': fuzzy.FuzzyDate(start_date=timezone.now().date()).fuzz(),
            'notes': fuzzy.FuzzyText(length=2048).fuzz(),
        }
        self.assertEqual(product.name, 'test')
        response = self.client.post(reverse('shopping-list-edit-product',
                                            kwargs={'product_id': product.id},
                                            host='my'),
                                    HTTP_HOST='my', data=data)
        self.assertEqual(response.status_code, 302)

    def test_product_edit_errors(self):
        shopping_list = ShoppingListFactory.create(user=self.user)
        product = ShoppingListProductFactory.create(shopping_list=shopping_list)

        data = {
            'name': fuzzy.FuzzyText(length=64).fuzz(),
            'shopping_list': shopping_list.id,
            'amount': fuzzy.FuzzyDecimal(low=-100, high=-1).fuzz(),
            'units': fuzzy.FuzzyChoice(dict(FridgeProduct.FridgeProductUnits.choices).keys()).fuzz(),
            'manufacture_date': fuzzy.FuzzyDate(start_date=timezone.now().date()).fuzz(),
            'shelf_life_date': fuzzy.FuzzyDate(start_date=timezone.now().date()).fuzz(),
            'notes': fuzzy.FuzzyText(length=2048).fuzz(),
        }
        response = self.client.post(reverse('shopping-list-edit-product',
                                            kwargs={'product_id': product.id},
                                            host='my'),
                                    HTTP_HOST='my', data=data)
        self.assertEqual(response.status_code, 200)

    def test_product_delete(self):
        shopping_list = ShoppingListFactory.create(user=self.user)
        product = ShoppingListProductFactory.create(shopping_list=shopping_list)

        prev_counter = ShoppingListProduct.objects.all().count()
        response = self.client.get(reverse('shopping-list-delete-product',
                                           kwargs={'product_id': product.id}, host='my'),
                                   HTTP_HOST='my')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('shopping-list', host='my'))

        new_counter = ShoppingListProduct.objects.all().count()
        self.assertTrue(prev_counter > new_counter)

    def test_product_check(self):
        shopping_list = ShoppingListFactory.create(user=self.user)
        product = ShoppingListProductFactory.create(shopping_list=shopping_list, is_checked=False)

        response = self.client.get(reverse('shopping-list-check-product',
                                           kwargs={'product_id': product.id}, host='my'),
                                   HTTP_HOST='my')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('shopping-list', host='my'))
        product.refresh_from_db()
        self.assertTrue(product.is_checked)

    def test_product_uncheck(self):
        shopping_list = ShoppingListFactory.create(user=self.user)
        product = ShoppingListProductFactory.create(shopping_list=shopping_list, is_checked=True)

        response = self.client.get(reverse('shopping-list-uncheck-product',
                                           kwargs={'product_id': product.id}, host='my'),
                                   HTTP_HOST='my')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('shopping-list', host='my'))
        product.refresh_from_db()
        self.assertFalse(product.is_checked)

    def test_product_edit_qty(self):
        shopping_list = ShoppingListFactory.create(user=self.user)
        product = ShoppingListProductFactory.create(shopping_list=shopping_list, name='test', amount=1)

        data = {
            'amount': 2,
        }
        self.assertEqual(product.amount, 1)
        response = self.client.post(reverse('shopping-list-change-qty-product',
                                            kwargs={'product_id': product.id},
                                            host='my'),
                                    HTTP_HOST='my', data=data)
        self.assertEqual(response.status_code, 200)
        product.refresh_from_db()
        self.assertEqual(product.amount, 2)

    def test_add_product_to_shopping_list(self):
        ShoppingListFactory.create(user=self.user)
        product = FridgeProductFactory.create(user=self.user)

        response = self.client.post(reverse('add-product-to-shopping-list',
                                            kwargs={'product_id': product.id},
                                            host='my'),
                                    HTTP_HOST='my', data={'_cancel': True})
        self.assertEqual(response.status_code, 302)
