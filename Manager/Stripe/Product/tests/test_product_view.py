from factory import fuzzy
from django.test import Client, TestCase
from django_hosts.resolvers import reverse

from core.User.factories import UserFactory
from core.Finances.factories import ProductFactory


class ProductViewTest(TestCase):
    def setUp(self):
        password = 'My0ldPassword@'

        self.user = UserFactory.create(is_superuser=True, is_staff=True, is_active=True, password=password)
        self.user.set_password(password)
        self.user.save()

        self.client = Client()
        self.client.force_login(user=self.user)

        self.product = ProductFactory.create()

    def test_view_list_get_success(self):
        response = self.client.get(reverse('manager-stripe-product-list', host='manager'), HTTP_HOST='manager')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.id)

    def test_view_success(self):
        response = self.client.get(
            reverse('manager-stripe-product-view', args=[self.product.id], host='manager'),
            HTTP_HOST='manager')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.id)

    def test_view_archive(self):
        response = self.client.get(
            reverse('manager-stripe-product-archive', args=[self.product.id], host='manager'),
            HTTP_HOST='manager')
        self.assertEqual(response.status_code, 302)
        self.product.refresh_from_db()
        self.assertFalse(self.product.is_active())

    def test_view_set_as_default(self):
        response = self.client.get(
            reverse('manager-stripe-product-set-as-default', args=[self.product.id], host='manager'),
            HTTP_HOST='manager')
        self.assertEqual(response.status_code, 302)
        self.product.refresh_from_db()
        self.assertTrue(self.product.is_default)
