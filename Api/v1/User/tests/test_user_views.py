from django.test import TestCase

from core.User.factories import UserFactory
from Api.v1.tests.base_test_case import ReadOnlyViewSetMixinTestCase


class UsersTestCase(ReadOnlyViewSetMixinTestCase, TestCase):

    def setup_user(self):
        super().setup_user()
        user = self.user
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.user = user

    def setUp(self) -> None:
        super().setUp()
        self.base_route = 'users'
        self.instance = UserFactory.create()

    def archive_instance(self):
        instance = self.instance
        instance.is_active = False
        instance.save()
        instance.refresh_from_db()
