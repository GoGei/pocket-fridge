import uuid

from django.test import TestCase

from ..models import User
from ..factories import UserFactory, StaffFactory, SuperuserFactory


class UserTests(TestCase):
    def test_create(self):
        obj = UserFactory.create()
        qs = User.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = UserFactory.create()
        obj.delete()

        qs = User.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())

    def test_str(self):
        obj = UserFactory.create()
        self.assertTrue(obj.email in str(obj))
        self.assertTrue(obj.email in obj.label)

    def test_full_name(self):
        first_name = 'First'
        last_name = 'Last'
        email = 'email%s@example.com'
        i = 0

        obj = UserFactory.create(first_name=first_name, last_name=None, email=email % str(i))
        self.assertEqual(email % str(i), obj.full_name)
        i += 1

        obj = UserFactory.create(first_name=None, last_name=last_name, email=email % str(i))
        self.assertEqual(email % str(i), obj.full_name)
        i += 1

        obj = UserFactory.create(first_name=first_name, last_name=last_name, email=email % str(i))
        self.assertTrue(all([item in obj.full_name for item in (first_name, last_name)]))

    def test_is_manager(self):
        user = UserFactory.create()
        staff = StaffFactory.create()
        superuser = SuperuserFactory.create()

        self.assertFalse(user.is_manager)
        self.assertTrue(staff.is_manager)
        self.assertTrue(superuser.is_manager)

    def test_qs(self):
        user = UserFactory.create()
        staff = StaffFactory.create(is_active=False)
        superuser = SuperuserFactory.create()

        admins = User.objects.admins()
        self.assertFalse(user in admins)
        self.assertTrue(staff in admins)
        self.assertTrue(superuser in admins)

        users = User.objects.users()
        self.assertTrue(user in users)
        self.assertFalse(staff in users)
        self.assertFalse(superuser in users)

        active = User.objects.active()
        self.assertTrue(user in active)
        self.assertFalse(staff in active)
        self.assertTrue(superuser in active)

    def test_create_superuser(self):
        email = 'email@example.com'
        password = str(uuid.uuid4())
        superuser = User.objects.create_superuser(email=email, password=password)
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

        self.assertRaises(ValueError, User.objects.create_superuser, email=email, password=password, is_staff=False)
        self.assertRaises(ValueError, User.objects.create_superuser, email=email, password=password, is_superuser=False)

    def test_create_user(self):
        email = 'email%s@example.com'
        password = str(uuid.uuid4())
        user = User.objects.create_user(email=email, password=password)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        user = User.objects.create_user(email='superuser@example.com', password=password,
                                        is_staff=True, is_superuser=True)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_user_no_email(self):
        password = str(uuid.uuid4())
        self.assertRaises(ValueError, User.objects.create_user, email=None, password=password)
        self.assertRaises(ValueError, User.objects.create_superuser, email=None, password=password)
