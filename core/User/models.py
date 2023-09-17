from django.db import models
from django.db.models import Q
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
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    phone = models.CharField(max_length=50, unique=True, db_index=True, null=True)
    # username = models.CharField(max_length=255, unique=True, db_index=True, null=True)
    # photo = models.ImageField(null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

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
