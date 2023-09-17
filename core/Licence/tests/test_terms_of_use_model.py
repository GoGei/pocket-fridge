from django.test import TestCase

from ..models import TermsOfUse
from ..factories import TermsOfUseFactory


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
