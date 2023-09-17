from factory import django, fuzzy

from django.conf import settings
from core.Currency.models import Currency


class CurrencyFactory(django.DjangoModelFactory):
    class Meta:
        model = Currency
        django_get_or_create = ('code',)

    name = fuzzy.FuzzyText(length=64)
    code = fuzzy.FuzzyText(length=4)
    number = fuzzy.FuzzyText(length=4)


class CurrencyDefaultFactory(CurrencyFactory):
    code = settings.DEFAULT_CURRENCY_CODE
    name = settings.DEFAULT_CURRENCY_NAME
    number = settings.DEFAULT_CURRENCY_NUMBER
