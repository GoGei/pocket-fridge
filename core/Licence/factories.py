from factory import fuzzy, SubFactory, DjangoModelFactory, django
from factory.faker import Faker
from core.User.factories import UserFactory
from .models import LicenceVersion, Licence, PrivacyPolicy, TermsOfUse


class LicenceVersionFactory(DjangoModelFactory):
    name = fuzzy.FuzzyText(length=8)
    slug = Faker('slug')

    class Meta:
        model = LicenceVersion
        django_get_or_create = ('slug',)


class LicenceFactory(DjangoModelFactory):
    name = fuzzy.FuzzyText(length=8)
    user = SubFactory(UserFactory)
    version = SubFactory(LicenceVersionFactory)

    class Meta:
        model = Licence


class PrivacyPolicyFactory(DjangoModelFactory):
    name = fuzzy.FuzzyText(length=8)
    template = django.FileField()
    version = SubFactory(LicenceVersionFactory)

    class Meta:
        model = PrivacyPolicy


class TermsOfUseFactory(DjangoModelFactory):
    name = fuzzy.FuzzyText(length=8)
    template = django.FileField()
    version = SubFactory(LicenceVersionFactory)

    class Meta:
        model = TermsOfUse
