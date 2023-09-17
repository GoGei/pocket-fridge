from django.test import TestCase

from ..models import LicenceVersion
from ..factories import LicenceVersionFactory


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
