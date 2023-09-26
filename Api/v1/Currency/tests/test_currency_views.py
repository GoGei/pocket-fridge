from django.test import TestCase
from rest_framework import status

from Api.v1.tests.base_test_case import ReadOnlyViewSetMixinTestCase
from core.Currency.factories import CurrencyFactory


class CurrencyTestCase(ReadOnlyViewSetMixinTestCase, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.base_route = 'currencies'
        self.instance = CurrencyFactory.create()
        self.client.logout()

    def test_list(self):
        response = self.client.get(self.get_list_url(), HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.json()
        self.assertTrue(result['count'])

    def test_list_not_found(self):
        pass

    def test_detail(self):
        response = self.client.get(self.get_detail_url(),
                                   HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.instance.code)
