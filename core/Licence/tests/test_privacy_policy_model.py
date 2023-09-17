from django.test import TestCase

from ..models import PrivacyPolicy
from ..factories import PrivacyPolicyFactory


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
