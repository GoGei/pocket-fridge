import factory
from factory import faker
from .models import User
from core.Utils.Tests.fuzzy_fields import FuzzyEmail


class UserFactory(factory.DjangoModelFactory):
    email = FuzzyEmail()
    first_name = faker.Faker('first_name')
    last_name = faker.Faker('last_name')
    # phone = FuzzyPhone()

    is_active = True
    is_staff = False
    is_superuser = False

    class Meta:
        model = User


class StaffFactory(UserFactory):
    is_staff = True
    is_superuser = False


class SuperuserFactory(UserFactory):
    is_staff = True
    is_superuser = True
