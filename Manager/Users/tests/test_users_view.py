from django.test import Client, TestCase
from django_hosts.resolvers import reverse

from core.User.factories import UserFactory


class UserViewTest(TestCase):
    def setUp(self):
        password = 'My0ldPassword@'

        self.user = UserFactory.create(is_superuser=True, is_staff=True, is_active=True, password=password)
        self.user.set_password(password)
        self.user.save()

        self.client = Client()
        self.client.force_login(user=self.user)

        self.user = UserFactory.create()

    def test_view_list_get_success(self):
        response = self.client.get(reverse('manager-users-list', host='manager'), HTTP_HOST='manager')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.id)

    def test_view_success(self):
        response = self.client.get(
            reverse('manager-users-view', args=[self.user.id], host='manager'),
            HTTP_HOST='manager')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.id)
