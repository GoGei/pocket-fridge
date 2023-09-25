from django.test import Client
from django.test import TestCase
from django_hosts.resolvers import reverse


class PublicViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_home_index_get_success(self):
        response = self.client.get(reverse('home-index', host='public'), HTTP_HOST='public')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Public/home_index.html')
