from django.test import Client, TestCase
from django_hosts.resolvers import reverse

from core.User.factories import UserFactory


class HomeViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.client = Client()
        self.client.force_login(self.user)

    def test_logout_view(self):
        response = self.client.post(reverse('manager-logout', host='manager'), HTTP_HOST='manager')
        self.assertEqual(response.status_code, 302)
