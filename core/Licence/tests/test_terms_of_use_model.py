from django.test import TestCase

from ..models import TermsOfUse
from ..factories import TermsOfUseFactory, LicenceVersionFactory


class TermsOfUseTests(TestCase):
    def test_create(self):
        obj = TermsOfUseFactory.create()
        qs = TermsOfUse.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = TermsOfUseFactory.create()
        obj.delete()

        qs = TermsOfUse.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())

    def test_set_default(self):
        version = LicenceVersionFactory.create()
        obj = TermsOfUseFactory.create(is_default=False, version=version)
        prev_default = TermsOfUseFactory.create(is_default=True, version=version)
        another = TermsOfUseFactory.create(is_default=False, version=version)

        obj.set_default()
        obj.refresh_from_db()
        prev_default.refresh_from_db()
        another.refresh_from_db()
        self.assertTrue(obj.is_default)
        self.assertFalse(prev_default.is_default)
        self.assertFalse(another.is_default)
