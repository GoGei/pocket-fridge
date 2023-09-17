from django.test import TestCase

from ..models import PrivacyPolicy
from ..factories import PrivacyPolicyFactory, LicenceVersionFactory


class PrivacyPolicyTests(TestCase):
    def test_create(self):
        obj = PrivacyPolicyFactory.create()
        qs = PrivacyPolicy.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = PrivacyPolicyFactory.create()
        obj.delete()

        qs = PrivacyPolicy.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())

    def test_set_default(self):
        version = LicenceVersionFactory.create()
        obj = PrivacyPolicyFactory.create(is_default=False, version=version)
        prev_default = PrivacyPolicyFactory.create(is_default=True, version=version)
        another = PrivacyPolicyFactory.create(is_default=False, version=version)

        obj.set_default()
        obj.refresh_from_db()
        prev_default.refresh_from_db()
        another.refresh_from_db()
        self.assertTrue(obj.is_default)
        self.assertFalse(prev_default.is_default)
        self.assertFalse(another.is_default)
