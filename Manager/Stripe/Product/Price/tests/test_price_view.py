from django.test import Client, TestCase
from django_hosts.resolvers import reverse

from core.User.factories import UserFactory
from core.Finances.factories import PriceFactory


class PriceViewTest(TestCase):
    def setUp(self):
        password = 'My0ldPassword@'

        self.user = UserFactory.create(is_superuser=True, is_staff=True, is_active=True, password=password)
        self.user.set_password(password)
        self.user.save()

        self.client = Client()
        self.client.force_login(user=self.user)

        self.price = PriceFactory.create()

    def test_view_success(self):
        response = self.client.get(
            reverse('manager-stripe-product-price-view', args=[self.price.id], host='manager'),
            HTTP_HOST='manager')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.price.id)

    def test_view_archive(self):
        response = self.client.get(
            reverse('manager-stripe-product-price-archive', args=[self.price.id], host='manager'),
            HTTP_HOST='manager')
        self.assertEqual(response.status_code, 302)
        self.price.refresh_from_db()
        self.assertFalse(self.price.is_active())

    def test_view_set_as_default(self):
        response = self.client.get(
            reverse('manager-stripe-product-price-set-as-default', args=[self.price.id], host='manager'),
            HTTP_HOST='manager')
        self.assertEqual(response.status_code, 302)
        self.price.refresh_from_db()
        self.assertTrue(self.price.is_default)
