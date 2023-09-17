from django.test import TestCase

from ..models import Licence
from ..factories import LicenceFactory


class LicenceTests(TestCase):
    def test_create(self):
        obj = LicenceFactory.create()
        qs = Licence.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = LicenceFactory.create()
        obj.delete()

        qs = Licence.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())
