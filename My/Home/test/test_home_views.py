from django.test import Client, TestCase
from django_hosts.resolvers import reverse

from core.User.factories import UserFactory
from core.Fridge.factories import FridgeTypeFactory


class HomeViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.client = Client()
        self.client.force_login(self.user)
        FridgeTypeFactory.create()
        self.user.activate()

    def test_logout_view(self):
        response = self.client.post(reverse('logout', host='my'), HTTP_HOST='my')
        self.assertEqual(response.status_code, 302)
