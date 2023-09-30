from django.test import Client, TestCase
from django_hosts.resolvers import reverse

from core.User.factories import UserFactory
from core.User.models import User


class PublicViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_index_get_success(self):
        response = self.client.get(reverse('home-index', host='public'), HTTP_HOST='public')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Public/home_index.html')

    def test_forgot_password_success(self):
        response = self.client.get(reverse('forgot-password-success', host='public'), HTTP_HOST='public')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Public/auth/auth-forgot-password-success.html')

    def test_licences(self):
        response = self.client.get(reverse('licences', host='public'), HTTP_HOST='public')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Public/licences.html')

    def test_go_to_fridge_view(self):
        response = self.client.get(reverse('go-to-fridge', host='public'), HTTP_HOST='public')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home-index', host='my'))

    def test_logout(self):
        response = self.client.get(reverse('logout', host='public'), HTTP_HOST='public')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login', host='public'))


class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_post_success(self):
        password = 'Test0Metest@'
        response = self.client.post(reverse('register', host='public'), data={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'password': password,
            'confirm_password': password,
            'agree_checkbox': True,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('register-success', host='public'))

    def test_register_post_invalid_form(self):
        response = self.client.post(reverse('register', host='public'), data={})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Public/auth/auth-register.html')

    def test_register_activate_no_user(self):
        response = self.client.get(reverse('register-activate', args=['wrongkey'], host='public'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home-index', host='public'))

    def test_register_activate_user(self):
        user = UserFactory(is_active=False)
        key = user.generate_registration_key()
        response = self.client.get(reverse('register-activate', args=[key], host='public'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home-index', host='public'))
        user.refresh_from_db()
        self.assertTrue(user.is_active)


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def test_authenticated_user_redirects_to_next_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('login') + '?next=/')
        self.assertRedirects(response, '/')

    def test_login_with_valid_credentials(self):
        data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'remember_me': False
        }
        response = self.client.post(reverse('login'), data)
        self.assertRedirects(response, reverse('home-index', host='my'))
        self.assertEqual(response.cookies['email'].value, 'test@example.com')

    def test_login_with_invalid_credentials(self):
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword',
            'remember_me': False
        }
        response = self.client.post(reverse('login'), data)
        self.assertFormError(response, 'form', None, 'User with this email and password not found')

    def test_inactive_user_login(self):
        self.user.is_active = False
        self.user.save()
        data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'remember_me': False
        }
        response = self.client.post(reverse('login'), data)
        # self.assertContains(response, 'User is not active! Please, contact a manager')
        self.assertContains(response, 'User with this email and password not found')

    def test_remember_me_checkbox(self):
        data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'remember_me': True
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.cookies['email'].value, 'test@example.com')


class ForgotPasswordTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_forgot_password_success(self):
        user = UserFactory.create()
        response = self.client.post(reverse('forgot-password'), data={'email': user.email})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('forgot-password-success', host='public'))

    def test_forgot_password_invalid_form(self):
        response = self.client.post(reverse('forgot-password'), data={})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Public/auth/auth-forgot-password.html')

    def test_forgot_password_reset(self):
        user = UserFactory(is_active=False)
        key = user.generate_forgot_password_key()
        password = 'Test0Metest@'
        data = {
            'password': password,
            'confirm_password': password,
        }
        response = self.client.post(reverse('forgot-password-reset', args=[key], host='public'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home-index', host='my'))

    def test_forgot_password_reset_wrong_key(self):
        response = self.client.get(reverse('forgot-password-reset', args=['wrongkey'], host='public'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home-index', host='public'))
