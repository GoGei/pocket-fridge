from factory import fuzzy
from django.test import Client, TestCase
from django_hosts.resolvers import reverse

from core.User.factories import UserFactory
from core.Fridge.factories import FridgeTypeFactory


class FridgeTypeViewTest(TestCase):
    def setUp(self):
        password = 'My0ldPassword@'

        self.user = UserFactory.create(is_superuser=True, is_staff=True, is_active=True, password=password)
        self.user.set_password(password)
        self.user.save()

        self.client = Client()
        self.client.force_login(user=self.user)

        self.fridge_type = FridgeTypeFactory.create()

        self.data = {
            'name': fuzzy.FuzzyText(length=50).fuzz(),
            'slug': fuzzy.FuzzyText(length=50).fuzz(),
            'create_on_user_creation': False,
        }

    def test_view_list_get_success(self):
        response = self.client.get(reverse('manager-fridge-type-list', host='manager'), HTTP_HOST='manager')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.fridge_type.id)

    def test_view_add_get_success(self):
        response = self.client.get(reverse('manager-fridge-type-add', host='manager'), HTTP_HOST='manager')
        self.assertEqual(response.status_code, 200)

    def test_view_add_post_success(self):
        data = self.data.copy()
        response = self.client.post(reverse('manager-fridge-type-add', host='manager'), HTTP_HOST='manager', data=data)
        self.assertEqual(response.status_code, 302)

    def test_view_add_post_cancel_success(self):
        response = self.client.post(reverse('manager-fridge-type-add', host='manager'), data={'_cancel': 'cancel'},
                                    HTTP_HOST='manager')
        self.assertEqual(response.status_code, 302)

    def test_view_edit_get_success(self):
        response = self.client.get(reverse('manager-fridge-type-edit', args=[self.fridge_type.id], host='manager'),
                                   HTTP_HOST='manager')
        self.assertEqual(response.status_code, 200)

    def test_view_edit_post_success(self):
        data = self.data.copy()
        response = self.client.post(reverse('manager-fridge-type-edit', args=[self.fridge_type.id], host='manager'),
                                    HTTP_HOST='manager', data=data)
        self.assertEqual(response.status_code, 302)

    def test_view_edit_post_cancel_success(self):
        response = self.client.post(reverse('manager-fridge-type-edit', args=[self.fridge_type.id], host='manager'),
                                    data={'_cancel': 'cancel'}, HTTP_HOST='manager')
        self.assertEqual(response.status_code, 302)

    def test_view_success(self):
        response = self.client.get(reverse('manager-fridge-type-view', args=[self.fridge_type.id], host='manager'),
                                   HTTP_HOST='manager')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.fridge_type.id)

    def test_view_archive(self):
        response = self.client.get(reverse('manager-fridge-type-archive', args=[self.fridge_type.id], host='manager'),
                                   HTTP_HOST='manager')
        self.assertEqual(response.status_code, 302)
        self.fridge_type.refresh_from_db()
        self.assertFalse(self.fridge_type.is_active())

    def test_view_restore(self):
        response = self.client.get(reverse('manager-fridge-type-restore', args=[self.fridge_type.id], host='manager'),
                                   HTTP_HOST='manager')
        self.assertEqual(response.status_code, 302)
        self.fridge_type.refresh_from_db()
        self.assertTrue(self.fridge_type.is_active())

    def test_view_fixture(self):
        response = self.client.get(reverse('manager-fridge-type-view-fixture', host='manager'),
                                   HTTP_HOST='manager')
        self.assertEqual(response.status_code, 200)

    def test_export_fixture(self):
        response = self.client.get(reverse('manager-fridge-type-export-to-fixture', host='manager'),
                                   HTTP_HOST='manager')
        self.assertEqual(response.status_code, 200)
