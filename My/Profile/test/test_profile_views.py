from django.test import Client, TestCase
from django_hosts.resolvers import reverse

from core.User.factories import UserFactory
from core.Fridge.factories import FridgeTypeFactory


class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.client = Client()
        self.client.force_login(self.user)
        FridgeTypeFactory.create()
        self.user.activate()

    def test_profile_view(self):
        response = self.client.post(reverse('profile', host='my'), HTTP_HOST='my')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'My/profile.html')

    def test_profile_export(self):
        response = self.client.post(reverse('profile-export', host='my'), HTTP_HOST='my')
        content = response.json()
        self.assertTrue(content)

    def test_logout_view(self):
        response = self.client.post(reverse('logout', host='my'), HTTP_HOST='my')
        self.assertEqual(response.status_code, 302)
