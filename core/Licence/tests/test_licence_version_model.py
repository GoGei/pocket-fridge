from django.test import TestCase

from ..models import LicenceVersion
from ..factories import LicenceVersionFactory, LicenceFactory


class LicenceVersionTests(TestCase):
    def test_create(self):
        obj = LicenceVersionFactory.create()
        qs = LicenceVersion.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = LicenceVersionFactory.create()
        obj.delete()

        qs = LicenceVersion.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())

    def test_str(self):
        obj = LicenceVersionFactory.create()
        self.assertIn(obj.name, str(obj))
        self.assertIn(obj.name, obj.label)

    def test_archive(self):
        obj = LicenceVersionFactory.create()
        licence = LicenceFactory.create(version=obj)
        obj.archive()
        obj.refresh_from_db()
        licence.refresh_from_db()
        self.assertFalse(obj.is_active())
        self.assertFalse(licence.is_active())

    def test_set_default(self):
        version1 = LicenceVersionFactory.create()
        version2 = LicenceVersionFactory.create()

        version1.set_default()
        version1.refresh_from_db()
        version2.refresh_from_db()
        self.assertTrue(version1.is_default)
        self.assertFalse(version2.is_default)
