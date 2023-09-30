from uuid import uuid4
from django.test import TestCase
from django_hosts import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.User.factories import UserFactory


class RegistrationTestCase(TestCase):
    def setUp(self) -> None:
        client = APIClient()
        self.client = client

    def test_register_all_errors(self):
        response = self.client.post(reverse('api-v1:register-register', host='api'), HTTP_HOST='api', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        keys = response.json().keys()
        error_fields = ['email', 'first_name', 'last_name', 'password', 'confirm_password']
        self.assertTrue(all(field in keys for field in error_fields))

    def test_register_password_error(self):
        data = {
            'email': 'test@gmail.com',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'password': str(uuid4()).replace('-', ''),
            'confirm_password': str(uuid4()).replace('-', ''),
        }
        response = self.client.post(reverse('api-v1:register-register', host='api'), HTTP_HOST='api', format='json',
                                    data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        keys = response.json().keys()
        error_fields = ['password', 'confirm_password']
        self.assertTrue(all(field in keys for field in error_fields))

    def test_register_email_error(self):
        user = UserFactory.create()
        data = {
            'email': user.email,
            'first_name': 'first_name',
            'last_name': 'last_name',
            'password': str(uuid4()).replace('-', ''),
            'confirm_password': str(uuid4()).replace('-', ''),
        }
        response = self.client.post(reverse('api-v1:register-register', host='api'), HTTP_HOST='api', format='json',
                                    data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        keys = response.json().keys()
        error_fields = ['email']
        self.assertTrue(all(field in keys for field in error_fields))

    def test_register(self):
        password = str(uuid4()).replace('-', '')[:15]
        data = {
            'email': 'test@gmail.com',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'password': password,
            'confirm_password': password,
        }
        response = self.client.post(reverse('api-v1:register-register', host='api'), HTTP_HOST='api', format='json',
                                    data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_activate_error_no_user(self):
        data = {
            'key': '',
        }
        response = self.client.post(reverse('api-v1:register-activate', host='api'), HTTP_HOST='api', format='json',
                                    data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_activate_error_active_user_found(self):
        user = UserFactory.create(is_active=True)
        key = user.generate_registration_key()
        data = {
            'key': key,
        }
        response = self.client.post(reverse('api-v1:register-activate', host='api'), HTTP_HOST='api', format='json',
                                    data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_activate(self):
        user = UserFactory.create(is_active=False)
        key = user.generate_registration_key()
        data = {
            'key': key,
        }
        response = self.client.post(reverse('api-v1:register-activate', host='api'), HTTP_HOST='api', format='json',
                                    data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertTrue(user.is_active)
