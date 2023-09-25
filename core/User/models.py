from __future__ import annotations
import time
from typing import Optional

import redis
import hashlib

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django_hosts.resolvers import reverse

from core.Fridge.models import Fridge
from core.Notifications.models import Notification
from core.Utils.Mixins.models import CrmMixin


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def admins(self):
        q = Q(is_superuser=True) | Q(is_staff=True)
        return self.filter(q)

    def users(self):
        q = Q(is_superuser=False) & Q(is_staff=False)
        return self.filter(q)

    def active(self):
        return self.filter(is_active=True)


class User(CrmMixin, AbstractBaseUser):
    """
    This is a User model class that inherits from CrmMixin and AbstractBaseUser.
    It represents a user in the system and has the following fields:

    - email: An email field that is unique and indexed in the database.
    - first_name: A character field for the user's first name.
    - last_name: A character field for the user's last name.
    - username: A character field for the user's username, which is unique and indexed in the database.
    - photo: An image field for the user's photo, which is uploaded to the specified directory.
    - is_active: A boolean field indicating whether the user is active or not.
    - is_staff: A boolean field indicating whether the user is a staff member or not.
    - is_superuser: A boolean field indicating whether the user is a superuser or not.
    - external_id: A character field for an external ID, which is unique and indexed in the database.
    """
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    username = models.CharField(max_length=255, unique=True, db_index=True, null=True)
    photo = models.ImageField(null=True, upload_to=settings.USER_PHOTO)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    external_id = models.CharField(max_length=32, null=True, unique=True, db_index=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    USER_REGISTRATION_ACCESS_KEY = 'user:registration:access-key:%s'
    USER_REGISTRATION_ACCESS_TTL = 60 * 60  # 1h
    USER_FORGOT_PASSWORD_KEY = 'user:forgot-password:key:%s'
    USER_FORGOT_PASSWORD_KEY_TTL = 24 * 60 * 60  # 24h

    objects = UserManager()

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email or self.id

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return ' '.join(list(map(str, [self.first_name, self.last_name])))
        return self.label

    @property
    def label(self):
        return str(self)

    @property
    def is_manager(self):
        return self.is_staff or self.is_superuser

    @property
    def notify_by_email(self):
        return self.email

    @property
    def licence_is_signed(self):
        from core.Licence.models import Licence, LicenceVersion
        version = LicenceVersion.get_default()
        return Licence.objects.select_related('user', 'version').active().filter(user=self, version=version).exists()

    def generate_registration_key(self) -> str:
        """
        Generate key for instance to register and put it to redis
        """
        key = hashlib.sha256(str(self.id).encode() + str(time.time()).encode()).hexdigest()
        redis_key = self.USER_REGISTRATION_ACCESS_KEY % key
        ttl = self.USER_REGISTRATION_ACCESS_TTL
        with redis.Redis() as r:
            r.setex(redis_key, ttl, self.id)
        return key

    def send_registration_email(self):
        key = self.generate_registration_key()
        url = reverse('api-v1:register-activate', host='api')
        schema = settings.SITE_SCHEME
        url = f'{schema}:{url}?key={key}'
        context = {
            'url': url,
            'key': key,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
        }
        notification = Notification.get_by_slug('registration-activate-email')
        notification.send(self, context)
        return notification

    @classmethod
    def get_by_registration_key(cls, key) -> Optional[User]:
        with redis.Redis() as r:
            redis_key = cls.USER_REGISTRATION_ACCESS_KEY % key
            user_id = r.get(redis_key)

        if not user_id:
            return None
        return cls.objects.filter(id=user_id).first()

    def activate(self):
        self.is_active = True
        self.save(update_fields=['is_active'])
        Fridge.create_fridges_for_user(self)
        return self

    @classmethod
    def clear_registration_keys(cls, key):
        with redis.Redis() as r:
            r.delete(cls.USER_REGISTRATION_ACCESS_KEY % key)

    def generate_forgot_password_key(self) -> str:
        key = hashlib.sha256(str(self.id).encode() + str(time.time()).encode()).hexdigest()
        redis_key = self.USER_FORGOT_PASSWORD_KEY % key
        ttl = self.USER_FORGOT_PASSWORD_KEY_TTL
        with redis.Redis() as r:
            r.setex(redis_key, ttl, self.id)
        return key

    def send_forgot_password_email(self):
        key = self.generate_forgot_password_key()
        url = reverse('forgot-password-reset', args=[key], host='public')
        schema = settings.SITE_SCHEME
        url = f'{schema}:{url}'
        context = {
            'url': url,
            'key': key,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
        }
        notification = Notification.get_by_slug('forgot-password-reset-email')
        notification.send(self, context)
        return notification

    @classmethod
    def get_by_forgot_password_key(cls, key) -> Optional[User]:
        with redis.Redis() as r:
            redis_key = cls.USER_FORGOT_PASSWORD_KEY % key
            user_id = r.get(redis_key)

        if not user_id:
            return None
        return cls.objects.filter(id=user_id).first()

    @classmethod
    def clear_forgot_password_keys(cls, key):
        with redis.Redis() as r:
            r.delete(cls.USER_FORGOT_PASSWORD_KEY % key)
