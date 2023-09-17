from django.test import TestCase

from ..models import Licence
from ..factories import LicenceFactory, DefaultLicenceVersionFactory
from core.User.factories import UserFactory


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

    def test_sign_licence_agreement(self):
        user = UserFactory.create()
        DefaultLicenceVersionFactory.create()
        self.assertFalse(user.licence_is_signed)
        Licence.sign_licence_agreement(user)
        self.assertTrue(user.licence_is_signed)
