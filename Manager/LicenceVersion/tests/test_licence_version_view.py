from factory import fuzzy
from django.test import Client, TestCase
from django_hosts.resolvers import reverse

from core.User.factories import UserFactory
from core.Licence.factories import LicenceVersionFactory, TermsOfUseFactory, PrivacyPolicyFactory


class LicenceVersionViewTest(TestCase):
    def setUp(self):
        password = 'My0ldPassword@'

        self.user = UserFactory.create(is_superuser=True, is_staff=True, is_active=True, password=password)
        self.user.set_password(password)
        self.user.save()

        self.client = Client()
        self.client.force_login(user=self.user)

        self.licence_version = LicenceVersionFactory.create()

        self.data = {
            'name': fuzzy.FuzzyText(length=30).fuzz(),
            'slug': fuzzy.FuzzyText(length=50).fuzz(),
            'is_default': False,
            'terms_of_use_template': TermsOfUseFactory.create().template,
            'privacy_policy_template': PrivacyPolicyFactory.create().template,
        }

    def test_view_list_get_success(self):
        response = self.client.get(reverse('manager-licence-version-list', host='manager'), HTTP_HOST='manager')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.licence_version.id)

    def test_view_add_get_success(self):
        response = self.client.get(reverse('manager-licence-version-add', host='manager'), HTTP_HOST='manager')
        self.assertEqual(response.status_code, 200)

    def test_view_add_post_success(self):
        data = self.data.copy()
        response = self.client.post(reverse('manager-licence-version-add', host='manager'), HTTP_HOST='manager',
                                    data=data)
        self.assertEqual(response.status_code, 302)

    def test_view_add_post_cancel_success(self):
        response = self.client.post(reverse('manager-licence-version-add', host='manager'), data={'_cancel': 'cancel'},
                                    HTTP_HOST='manager')
        self.assertEqual(response.status_code, 302)

    def test_view_edit_get_success(self):
        response = self.client.get(
            reverse('manager-licence-version-edit', args=[self.licence_version.id], host='manager'),
            HTTP_HOST='manager')
        self.assertEqual(response.status_code, 200)

    def test_view_edit_post_success(self):
        data = self.data.copy()
        TermsOfUseFactory.create(version=self.licence_version, is_default=True)
        PrivacyPolicyFactory.create(version=self.licence_version, is_default=True)
        response = self.client.post(
            reverse('manager-licence-version-edit', args=[self.licence_version.id], host='manager'),
            HTTP_HOST='manager', data=data)
        self.assertEqual(response.status_code, 302)

    def test_view_edit_post_cancel_success(self):
        response = self.client.post(
            reverse('manager-licence-version-edit', args=[self.licence_version.id], host='manager'),
            data={'_cancel': 'cancel'}, HTTP_HOST='manager')
        self.assertEqual(response.status_code, 302)

    def test_view_success(self):
        response = self.client.get(
            reverse('manager-licence-version-view', args=[self.licence_version.id], host='manager'),
            HTTP_HOST='manager')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.licence_version.id)

    def test_view_archive(self):
        response = self.client.get(
            reverse('manager-licence-version-archive', args=[self.licence_version.id], host='manager'),
            HTTP_HOST='manager')
        self.assertEqual(response.status_code, 302)
        self.licence_version.refresh_from_db()
        self.assertFalse(self.licence_version.is_active())

    def test_view_restore(self):
        response = self.client.get(
            reverse('manager-licence-version-restore', args=[self.licence_version.id], host='manager'),
            HTTP_HOST='manager')
        self.assertEqual(response.status_code, 302)
        self.licence_version.refresh_from_db()
        self.assertTrue(self.licence_version.is_active())
