"""
The code provided is a Django model implementation for handling finance integrations.
It includes several models such as Product, Price, Subscription, Invoice, and Payment,
all of which inherit from the FinanceIntegrationsMixin.
"""
from django.core.validators import MinValueValidator
from django.db import models
from core.Utils.Mixins.models import CrmMixin, UUIDPrimaryKeyMixin, ActiveQuerySet
from django.utils.translation import gettext_lazy as _


class FinanceIntegrationsQuerySet(ActiveQuerySet):
    def integrated(self):
        return self.filter(external_id__isnull=False)

    def not_integrated(self):
        return self.filter(external_id_isnull=True)


class FinanceIntegrationsMixin(CrmMixin, UUIDPrimaryKeyMixin):
    """
    The FinanceIntegrationsMixin includes a field called external_id, which is used to store an external identifier
    for each instance. It also provides methods for checking if an instance is integrated or not.
    """
    external_id = models.CharField(max_length=32, unique=True, db_index=True, null=True)
    objects = FinanceIntegrationsQuerySet.as_manager()

    @property
    def is_integrated(self):
        return bool(getattr(self, 'external_id', False))

    @property
    def is_not_integrated(self):
        return not bool(getattr(self, 'external_id', False))

    class Meta:
        abstract = True


class Product(FinanceIntegrationsMixin):
    """
    The Product model represents a product of a subscription.
    """
    name = models.CharField(max_length=64, db_index=True)
    description = models.CharField(max_length=2048)
    is_published = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = 'product'


class Price(FinanceIntegrationsMixin):
    """
    The Price model represents the pricing information for a product.
    """
    class PriceIntervalChoices(models.TextChoices):
        DAY = 'day', _('Day')
        # WEEK = 'week', 'W_(eek')
        MONTH = 'month', _('Month')
        YEAR = 'year', _('Year')

    class PriceUsageTypeChoices(models.TextChoices):
        # METERED = 'metered', 'M_(etered')
        LICENSED = 'licensed', _('Licensed')

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=16, decimal_places=2, db_index=True)
    currency = models.ForeignKey('Currency.Currency', on_delete=models.PROTECT)
    # recurring JSON data
    interval = models.CharField(choices=PriceIntervalChoices.choices, max_length=8)
    interval_count = models.IntegerField(default=1)
    usage_type = models.CharField(choices=PriceUsageTypeChoices.choices,
                                  default=PriceUsageTypeChoices.LICENSED,
                                  max_length=10)
    is_published = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = 'price'


class Subscription(FinanceIntegrationsMixin):
    """
    The Subscription model represents a subscription for a user to a product.
    """
    class SubscriptionCollectionMethodsChoices(models.TextChoices):
        CHARGE_AUTOMATICALLY = 'charge_automatically', _('Charge automatically')
        SEND_INVOICE = 'send_invoice', _('Send invoice')

    class SubscriptionStatusChoices(models.TextChoices):
        INCOMPLETE = 'incomplete', _('Incomplete')
        INCOMPLETE_EXPIRED = 'incomplete_expired', _('Incomplete expired')
        TRAILING = 'trialing', _('Trialing')
        ACTIVE = 'active', _('Active')
        PAST_DUE = 'past_due', _('Past due')
        CANCELED = 'canceled', _('Canceled')
        UNPAID = 'unpaid', _('Unpaid')

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.ForeignKey(Price, on_delete=models.PROTECT)
    currency = models.ForeignKey('Currency.Currency', on_delete=models.PROTECT)
    user = models.ForeignKey('User.User', on_delete=models.PROTECT)
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(null=True, db_index=True)
    quantity = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    collection_method = models.CharField(choices=SubscriptionCollectionMethodsChoices.choices,
                                         default=SubscriptionCollectionMethodsChoices.CHARGE_AUTOMATICALLY,
                                         max_length=24)
    next_billing_day = models.DateTimeField(null=True, db_index=True)
    status = models.CharField(choices=SubscriptionStatusChoices.choices,
                              default=SubscriptionStatusChoices.ACTIVE,
                              max_length=24)

    class Meta:
        db_table = 'subscription'


class Invoice(FinanceIntegrationsMixin):
    """
    The Invoice model represents an invoice for a user's subscription.
    """

    class InvoiceStatusChoices(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        OPEN = 'open', _('Open')
        PAID = 'paid', _('Paid')
        VOID = 'void', _('Void')
        UNCOLLECTIBLE = 'uncollectible', _('Uncollectible')

    number = models.CharField(max_length=64, unique=True, db_index=True, null=True)
    collection_method = models.CharField(choices=Subscription.SubscriptionCollectionMethodsChoices.choices,
                                         default=Subscription.SubscriptionCollectionMethodsChoices.CHARGE_AUTOMATICALLY,
                                         max_length=24)
    currency = models.ForeignKey('Currency.Currency', on_delete=models.PROTECT)
    user = models.ForeignKey('User.User', on_delete=models.PROTECT, db_index=True)
    customer_internal_id = models.CharField(max_length=32, db_index=True, null=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.PROTECT)
    status = models.CharField(choices=InvoiceStatusChoices.choices,
                              default=InvoiceStatusChoices.DRAFT,
                              max_length=16)
    total = models.DecimalField(max_digits=16, decimal_places=4, null=True)

    class Meta:
        db_table = 'invoice'


class Payment(FinanceIntegrationsMixin):
    """
    The Payment model represents a payment made for an invoice.
    """
    class PaymentIntentStatusChoices(models.TextChoices):
        REQUIRES_PAYMENT_METHOD = 'requires_payment_method', _('Requires payment method')
        REQUIRES_CONFIRMATION = 'requires_confirmation', _('Requires confirmation')
        REQUIRES_ACTION = 'requires_action', _('Requires action')
        PROCESSING = 'processing', _('Processing')
        REQUIRES_CAPTURE = 'requires_capture', _('Requires capture')
        CANCELED = 'canceled', _('Canceled')
        SUCCEEDED = 'succeeded', _('Succeeded')

    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, null=True)
    user = models.ForeignKey('User.User', on_delete=models.PROTECT)
    currency = models.ForeignKey('Currency.Currency', on_delete=models.PROTECT, null=True)
    status = models.CharField(choices=PaymentIntentStatusChoices.choices,
                              default=PaymentIntentStatusChoices.PROCESSING,
                              max_length=32)

    class Meta:
        db_table = 'payment'
