from factory import fuzzy, SubFactory, DjangoModelFactory, django
from factory.faker import Faker
from core.User.factories import UserFactory
from .models import LicenceVersion, Licence, PrivacyPolicy, TermsOfUse


class LicenceVersionFactory(DjangoModelFactory):
    name = fuzzy.FuzzyText(length=8)
    slug = Faker('slug')
    is_default = False

    class Meta:
        model = LicenceVersion
        django_get_or_create = ('slug',)


class DefaultLicenceVersionFactory(LicenceVersionFactory):
    is_default = True


class LicenceFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    version = SubFactory(LicenceVersionFactory)

    class Meta:
        model = Licence


class PrivacyPolicyFactory(DjangoModelFactory):
    name = fuzzy.FuzzyText(length=32)
    template = django.FileField()
    version = SubFactory(LicenceVersionFactory)
    is_default = False

    class Meta:
        model = PrivacyPolicy


class TermsOfUseFactory(DjangoModelFactory):
    name = fuzzy.FuzzyText(length=32)
    template = django.FileField()
    version = SubFactory(LicenceVersionFactory)
    is_default = False

    class Meta:
        model = TermsOfUse
