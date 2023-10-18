from factory import django, fuzzy, SubFactory, LazyAttribute
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from core.Currency.factories import CurrencyDefaultFactory
from core.User.factories import UserFactory

from .models import Product, Price, Subscription, Invoice, Payment


class ProductFactory(django.DjangoModelFactory):
    class Meta:
        model = Product

    external_id = fuzzy.FuzzyText(length=32)
    name = fuzzy.FuzzyText(length=64)
    description = fuzzy.FuzzyText(length=2000)
    is_default = False


class PriceFactory(django.DjangoModelFactory):
    class Meta:
        model = Price

    external_id = fuzzy.FuzzyText(length=32)
    product = SubFactory(ProductFactory)
    price = fuzzy.FuzzyDecimal(low=0.01, high=99999.99)
    currency = SubFactory(CurrencyDefaultFactory)
    interval = fuzzy.FuzzyChoice(choices=dict(Price.PriceIntervalChoices.choices).keys())
    interval_count = 1
    usage_type = fuzzy.FuzzyChoice(choices=dict(Price.PriceUsageTypeChoices.choices).keys())
    is_default = False


class SubscriptionFactory(django.DjangoModelFactory):
    class Meta:
        model = Subscription

    external_id = fuzzy.FuzzyText(length=32)
    product = SubFactory(ProductFactory)
    price = LazyAttribute(lambda obj: PriceFactory.create(product=obj.product))
    currency = SubFactory(CurrencyDefaultFactory)
    user = SubFactory(UserFactory)
    start_date = fuzzy.FuzzyDate(start_date=timezone.now().date() - timezone.timedelta(days=180))
    end_date = LazyAttribute(lambda obj:
                             obj.start_date + relativedelta(months=1) if
                             obj.price.interval == Price.PriceIntervalChoices.MONTH else
                             obj.start_date + relativedelta(years=1))
    quantity = fuzzy.FuzzyInteger(low=1, high=999)
    collection_method = fuzzy.FuzzyChoice(
        choices=dict(Subscription.SubscriptionCollectionMethodsChoices.choices).keys())
    next_billing_day = fuzzy.FuzzyDateTime(start_dt=timezone.now() + timezone.timedelta(days=1),
                                           end_dt=timezone.now() + timezone.timedelta(days=30))
    status = fuzzy.FuzzyChoice(choices=dict(Subscription.SubscriptionStatusChoices.choices).keys())


class InvoiceFactory(django.DjangoModelFactory):
    class Meta:
        model = Invoice

    external_id = fuzzy.FuzzyText(length=32)
    number = fuzzy.FuzzyText(length=64)
    collection_method = fuzzy.FuzzyChoice(choices=dict(Invoice.InvoiceStatusChoices.choices).keys())
    currency = SubFactory(CurrencyDefaultFactory)
    user = SubFactory(UserFactory)
    subscription = SubFactory(SubscriptionFactory)
    status = fuzzy.FuzzyChoice(choices=dict(Invoice.InvoiceStatusChoices.choices).keys())
    total = fuzzy.FuzzyDecimal(low=0.01, high=99999.99)


class PaymentFactory(django.DjangoModelFactory):
    class Meta:
        model = Payment

    external_id = fuzzy.FuzzyText(length=32)
    invoice = LazyAttribute(lambda obj: InvoiceFactory.create(user=obj.user))
    user = SubFactory(UserFactory)
    currency = SubFactory(CurrencyDefaultFactory)
    status = fuzzy.FuzzyChoice(choices=dict(Payment.PaymentIntentStatusChoices.choices).keys())
