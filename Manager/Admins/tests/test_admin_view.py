from factory import fuzzy
from django.test import Client, TestCase
from django_hosts.resolvers import reverse

from Manager.Admins.forms import StatusChoices
from core.User.factories import UserFactory


class AdminViewTest(TestCase):
    def setUp(self):
        password = 'My0ldPassword@'
        new_password = 'MyNewPassword0@'

        self.user = UserFactory.create(is_superuser=True, is_staff=True, is_active=True, password=password)
        self.user.set_password(password)
        self.user.save()

        self.client = Client()
        self.client.force_login(user=self.user)

        self.simple_user = UserFactory.create(is_superuser=False, is_staff=False, is_active=True)
        self.staff_user = UserFactory.create(is_superuser=False, is_staff=True, is_active=True)
        self.admin_user = UserFactory.create(is_superuser=True, is_staff=True, is_active=True, password=password)

        self.data = {
            'email': '%s@example.com' % fuzzy.FuzzyText(length=64).fuzz(),
            'password': password,
            'first_name': fuzzy.FuzzyText(length=50).fuzz(),
            'last_name': fuzzy.FuzzyText(length=50).fuzz(),
            'status': StatusChoices.STAFF,
            'is_active': False,
        }
        self.reset_password_data = {
            'current_password': password,
            'password': new_password,
            'confirm_password': new_password,
        }
        self.set_password_data = {
            'password': new_password,
            'confirm_password': new_password,
        }

    def test_view_list_get_success(self):
        response = self.client.get(reverse('manager-admins-list', host='manager'), HTTP_HOST='manager')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.simple_user.email)
        self.assertContains(response, self.staff_user.email)
        self.assertContains(response, self.admin_user.email)

    def test_view_add_get_success(self):
        response = self.client.get(reverse('manager-admins-add', host='manager'), HTTP_HOST='manager')
        self.assertEqual(response.status_code, 200)

    def test_view_add_post_success(self):
        data = self.data.copy()
        response = self.client.post(reverse('manager-admins-add', host='manager'), HTTP_HOST='manager', data=data)
        self.assertEqual(response.status_code, 302)

    def test_view_add_post_cancel_success(self):
        response = self.client.post(reverse('manager-admins-add', host='manager'), data={'_cancel': 'cancel'},
                                    HTTP_HOST='manager')
        self.assertEqual(response.status_code, 302)

    def test_view_edit_get_success(self):
        response = self.client.get(reverse('manager-admins-edit', args=[self.user.id], host='manager'),
                                   HTTP_HOST='manager')
        self.assertEqual(response.status_code, 200)

    def test_view_edit_post_success(self):
        data = self.data.copy()
        response = self.client.post(reverse('manager-admins-edit', args=[self.admin_user.id], host='manager'),
                                    HTTP_HOST='manager', data=data)
        self.assertEqual(response.status_code, 302)

    def test_view_edit_post_cancel_success(self):
        response = self.client.post(reverse('manager-admins-edit', args=[self.user.id], host='manager'),
                                    data={'_cancel': 'cancel'}, HTTP_HOST='manager')
        self.assertEqual(response.status_code, 302)

    def test_view_success(self):
        response = self.client.get(reverse('manager-admins-view', args=[self.user.id], host='manager'),
                                   HTTP_HOST='manager')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.id)

    def test_view_reset_password_get_success(self):
        response = self.client.get(reverse('manager-admins-reset-password', host='manager'),
                                   HTTP_HOST='manager')
        self.assertEqual(response.status_code, 200)

    def test_view_reset_password_post_success(self):
        data = self.reset_password_data.copy()
        response = self.client.post(reverse('manager-admins-reset-password', host='manager'),
                                    HTTP_HOST='manager', data=data)
        self.assertEqual(response.status_code, 302)

    def test_view_set_password_get_success(self):
        response = self.client.get(reverse('manager-admins-set-password', args=[self.user.id], host='manager'),
                                   HTTP_HOST='manager')
        self.assertEqual(response.status_code, 200)

    def test_view_set_password_post_success(self):
        data = self.set_password_data.copy()
        response = self.client.post(reverse('manager-admins-set-password', args=[self.user.id], host='manager'),
                                    HTTP_HOST='manager', data=data)
        self.assertEqual(response.status_code, 302)
