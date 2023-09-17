from factory import django, fuzzy, SubFactory

from django.conf import settings
from django.utils import timezone
from core.Currency.models import Currency, CurrencyExchange


class CurrencyFactory(django.DjangoModelFactory):
    class Meta:
        model = Currency
        django_get_or_create = ('code',)

    name = fuzzy.FuzzyText(length=64)
    code = fuzzy.FuzzyText(length=4)
    number = fuzzy.FuzzyText(length=4)


class CurrencyDefaultFactory(CurrencyFactory):
    code = settings.DEFAULT_CURRENCY
    name = 'US Dollar'


class CurrencyExchangeFactory(django.DjangoModelFactory):
    class Meta:
        model = CurrencyExchange

    source_currency = SubFactory(CurrencyFactory)
    target_currency = SubFactory(CurrencyFactory)
    start_date = fuzzy.FuzzyDate(timezone.now().date())
    rate = fuzzy.FuzzyDecimal(low=0.0, high=999999.9999)
