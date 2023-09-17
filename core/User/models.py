from django.db import models
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
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
