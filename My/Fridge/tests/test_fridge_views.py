from django.utils import timezone
from factory import fuzzy
from django.test import Client, TestCase
from django_hosts.resolvers import reverse

from core.User.factories import UserFactory
from core.Fridge.models import FridgeProduct
from core.Fridge.factories import FridgeTypeFactory, FridgeFactory, FridgeProductFactory


class FridgeViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.client = Client()
        self.client.force_login(self.user)
        FridgeTypeFactory.create()
        self.user.activate()

    def test_fridge_add(self):
        response = self.client.post(reverse('fridge-add', host='my'), HTTP_HOST='my')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'My/Fridge/fridge_add.html')

    def test_fridge_add_cancel(self):
        response = self.client.post(reverse('fridge-add', host='my'), HTTP_HOST='my', data={'_cancel': True})
        self.assertEqual(response.status_code, 302)
        # self.assertRedirects(response, reverse('home-index', host='my'))

    def test_fridge_add_success(self):
        fridge = FridgeFactory.create(user=self.user)
        data = {
            'name': fuzzy.FuzzyText(length=64).fuzz(),
            'fridge': fridge.id,
            'amount': fuzzy.FuzzyDecimal(low=1, high=100).fuzz(),
            'units': fuzzy.FuzzyChoice(dict(FridgeProduct.FridgeProductUnits.choices).keys()).fuzz(),
            'manufacture_date': fuzzy.FuzzyDate(start_date=timezone.now().date()).fuzz(),
            'shelf_life_date': fuzzy.FuzzyDate(start_date=timezone.now().date()).fuzz(),
            'notes': fuzzy.FuzzyText(length=2048).fuzz(),
        }

        prev_counter = FridgeProduct.objects.all().count()

        response = self.client.post(reverse('fridge-add', host='my'), HTTP_HOST='my', data=data)
        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, reverse('fridge-view', kwargs={'fridge_id': fridge.id}, host='my'))

        new_counter = FridgeProduct.objects.all().count()
        self.assertTrue(new_counter > prev_counter)

    def test_fridge_add_errors(self):
        fridge = FridgeFactory.create(user=self.user)
        data = {
            'name': fuzzy.FuzzyText(length=64).fuzz(),
            'fridge': fridge.id,
            'amount': fuzzy.FuzzyDecimal(low=-100, high=-1).fuzz(),
            'units': fuzzy.FuzzyChoice(dict(FridgeProduct.FridgeProductUnits.choices).keys()).fuzz(),
            'manufacture_date': fuzzy.FuzzyDate(start_date=timezone.now().date()).fuzz(),
            'shelf_life_date': fuzzy.FuzzyDate(start_date=timezone.now().date()).fuzz(),
            'notes': fuzzy.FuzzyText(length=2048).fuzz(),
        }

        prev_counter = FridgeProduct.objects.all().count()

        response = self.client.post(reverse('fridge-add', host='my'), HTTP_HOST='my', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Amount cannot be negative')

        new_counter = FridgeProduct.objects.all().count()
        self.assertTrue(new_counter == prev_counter)

    def test_fridge_with_id_add_success(self):
        fridge = FridgeFactory.create(user=self.user)
        data = {
            'name': fuzzy.FuzzyText(length=64).fuzz(),
            'fridge': fridge.id,
            'amount': fuzzy.FuzzyDecimal(low=1, high=100).fuzz(),
            'units': fuzzy.FuzzyChoice(dict(FridgeProduct.FridgeProductUnits.choices).keys()).fuzz(),
            'manufacture_date': fuzzy.FuzzyDate(start_date=timezone.now().date()).fuzz(),
            'shelf_life_date': fuzzy.FuzzyDate(start_date=timezone.now().date()).fuzz(),
            'notes': fuzzy.FuzzyText(length=2048).fuzz(),
        }

        prev_counter = FridgeProduct.objects.all().count()

        response = self.client.post(reverse('fridge-add-for-fridge', args=[fridge.id], host='my'), HTTP_HOST='my',
                                    data=data)
        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, reverse('fridge-view', kwargs={'fridge_id': fridge.id}, host='my'))

        new_counter = FridgeProduct.objects.all().count()
        self.assertTrue(new_counter > prev_counter)

    def test_fridge_with_id_add_errors(self):
        fridge = FridgeFactory.create(user=self.user)
        data = {
            'name': fuzzy.FuzzyText(length=64).fuzz(),
            'fridge': fridge.id,
            'amount': fuzzy.FuzzyDecimal(low=-100, high=-1).fuzz(),
            'units': fuzzy.FuzzyChoice(dict(FridgeProduct.FridgeProductUnits.choices).keys()).fuzz(),
            'manufacture_date': fuzzy.FuzzyDate(start_date=timezone.now().date()).fuzz(),
            'shelf_life_date': fuzzy.FuzzyDate(start_date=timezone.now().date()).fuzz(),
            'notes': fuzzy.FuzzyText(length=2048).fuzz(),
        }

        prev_counter = FridgeProduct.objects.all().count()

        response = self.client.post(reverse('fridge-add-for-fridge', args=[fridge.id], host='my'), HTTP_HOST='my',
                                    data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Amount cannot be negative')

        new_counter = FridgeProduct.objects.all().count()
        self.assertTrue(new_counter == prev_counter)

    def test_fridge_view(self):
        fridge = FridgeFactory.create(user=self.user)
        product = FridgeProductFactory.create(fridge=fridge)
        response = self.client.get(reverse('fridge-view', kwargs={'fridge_id': fridge.id}, host='my'), HTTP_HOST='my')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, fridge.id)
        self.assertContains(response, product.id)

    def test_product_view(self):
        fridge = FridgeFactory.create(user=self.user)
        product = FridgeProductFactory.create(fridge=fridge)
        response = self.client.get(reverse('product-view',
                                           kwargs={'fridge_id': fridge.id, 'product_id': product.id}, host='my'),
                                   HTTP_HOST='my')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, fridge.id)
        self.assertContains(response, product.id)

    def test_product_edit(self):
        fridge = FridgeFactory.create(user=self.user)
        product = FridgeProductFactory.create(fridge=fridge)
        response = self.client.post(reverse('product-edit',
                                            kwargs={'fridge_id': fridge.id, 'product_id': product.id}, host='my'),
                                    HTTP_HOST='my', data={'_cancel': True})
        self.assertEqual(response.status_code, 302)

    def test_product_edit_success(self):
        fridge = FridgeFactory.create(user=self.user)
        product = FridgeProductFactory.create(fridge=fridge, name='test')

        data = {
            'name': fuzzy.FuzzyText(length=64).fuzz(),
            'fridge': fridge.id,
            'amount': fuzzy.FuzzyDecimal(low=1, high=100).fuzz(),
            'units': fuzzy.FuzzyChoice(dict(FridgeProduct.FridgeProductUnits.choices).keys()).fuzz(),
            'manufacture_date': fuzzy.FuzzyDate(start_date=timezone.now().date()).fuzz(),
            'shelf_life_date': fuzzy.FuzzyDate(start_date=timezone.now().date()).fuzz(),
            'notes': fuzzy.FuzzyText(length=2048).fuzz(),
        }
        self.assertEqual(product.name, 'test')
        response = self.client.post(reverse('product-edit',
                                            kwargs={'fridge_id': fridge.id, 'product_id': product.id}, host='my'),
                                    HTTP_HOST='my', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             reverse('product-view', kwargs={'fridge_id': fridge.id, 'product_id': product.id},
                                     host='my'))
        product.refresh_from_db()
        self.assertEqual(len(product.name), 64)

    def test_product_edit_errors(self):
        fridge = FridgeFactory.create(user=self.user)
        product = FridgeProductFactory.create(fridge=fridge)

        data = {
            'name': fuzzy.FuzzyText(length=64).fuzz(),
            'fridge': fridge.id,
            'amount': fuzzy.FuzzyDecimal(low=-100, high=-1).fuzz(),
            'units': fuzzy.FuzzyChoice(dict(FridgeProduct.FridgeProductUnits.choices).keys()).fuzz(),
            'manufacture_date': fuzzy.FuzzyDate(start_date=timezone.now().date()).fuzz(),
            'shelf_life_date': fuzzy.FuzzyDate(start_date=timezone.now().date()).fuzz(),
            'notes': fuzzy.FuzzyText(length=2048).fuzz(),
        }
        response = self.client.post(reverse('product-edit',
                                            kwargs={'fridge_id': fridge.id, 'product_id': product.id}, host='my'),
                                    HTTP_HOST='my', data=data)
        self.assertEqual(response.status_code, 200)

    def test_product_delete(self):
        fridge = FridgeFactory.create(user=self.user)
        product = FridgeProductFactory.create(fridge=fridge)

        prev_counter = FridgeProduct.objects.all().count()
        response = self.client.get(reverse('product-delete',
                                           kwargs={'fridge_id': fridge.id, 'product_id': product.id}, host='my'),
                                   HTTP_HOST='my')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('fridge-view', kwargs={'fridge_id': fridge.id}, host='my'))

        new_counter = FridgeProduct.objects.all().count()
        self.assertTrue(prev_counter > new_counter)
