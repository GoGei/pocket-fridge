from decimal import Decimal

import pytz
import stripe
from stripe import error
from datetime import datetime
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from . import exceptions
from .mixins import StripeMixin

from core.Finances.models import Product, Price, Subscription, Invoice, Payment
from core.Currency.models import Currency
from core.User.models import User


def int_to_timestamp(value: int):
    if not value:
        return None

    value = datetime.utcfromtimestamp(value)
    tz = pytz.timezone(settings.TIME_ZONE_DEFAULT)
    value = value.astimezone(tz)
    return value


class ProductHandler(StripeMixin):
    """
    https://stripe.com/docs/api/products
    """
    model = stripe.Product

    def instance_to_stripe(self, instance: Product) -> dict:
        response = {
            'name': instance.name,
            'active': instance.is_active,
            'description': instance.description or '',
            'metadata': {
                'is_default': instance.is_default,
            }
        }
        return response

    def update_instance(self, data, instance: Product) -> Product:
        instance.external_id = data['id']
        instance.name = data['name']
        instance.description = data['description']

        metadata = data.get('metadata', {})
        is_default = metadata.get('is_default', False)
        if is_default:
            instance.set_as_default()

        active = data['active']
        if not active:
            instance.is_published = False
            instance.archive()
        elif active and not instance.is_active:
            instance.is_published = True
            instance.restore()

        return instance


class PriceHandler(StripeMixin):
    """
    https://stripe.com/docs/api/prices
    """
    model = stripe.Price

    def instance_to_stripe(self, instance: Price) -> dict:
        response = {
            'currency': instance.currency.code,
            'product': instance.product.external_id,
            'active': instance.is_active,
            'recurring': instance.recurring,
            'unit_amount_decimal': instance.stripify_price,
            'metadata': {
                'is_default': instance.is_default,
            }
        }

        return response

    def update_instance(self, data, instance: Price) -> Price:
        instance.external_id = data['id']

        instance.currency = Currency.objects.get(code__iexact=data['currency'])
        instance.product = Product.objects.get(internal_id=data['product'])
        recurring = data['recurring']
        instance.interval = recurring['interval']
        instance.interval_count = recurring['interval_count']
        instance.usage_type = recurring['usage_type']
        instance.price = Price.unstripify_price(data['unit_amount_decimal'])
        instance.save()

        active = data['active']
        if not active:
            instance.archive()
        elif active and not instance.is_active:
            instance.restore()

        metadata = data.get('metadata', {})
        is_default = metadata.get('is_default', False)
        if is_default:
            instance.set_as_default()

        return instance


class SubscriptionHandler(StripeMixin):
    """
    https://stripe.com/docs/api/subscriptions
    """
    model = stripe.Subscription

    def instance_to_stripe(self, instance: Subscription) -> dict:
        response = {
            'customer': instance.user.external_id,
            'items': [{'price': instance.price.external_id, 'quantity': instance.quantity}],
            'currency': instance.currency.code,
        }

        return response

    def update_instance(self, data, instance: Subscription) -> Subscription:
        instance.external_id = data['id']

        item_data = data['items']['data'][0]
        price_data = item_data['price']

        try:
            instance.product = Product.objects.get(internal_id=price_data['product'])
        except Product.DoesNotExist:
            raise exceptions.StripeObjectNotFound(_('Product not found'))

        try:
            instance.price = Price.objects.get(internal_id=price_data['id'])
        except Price.DoesNotExist:
            raise exceptions.StripeObjectNotFound(_('Price not found'))

        instance.currency = Currency.objects.get(code__iexact=price_data['currency'])

        try:
            instance.user = User.objects.get(external_id=data['customer'])
        except User.DoesNotExist:
            raise exceptions.StripeObjectNotFound(_('Customer not found'))

        instance.start_date = int_to_timestamp(data.get('created'))
        instance.end_date = int_to_timestamp(data.get('ended_at'))
        instance.quantity = data.get('quantity')
        instance.collection_method = data.get('collection_method')
        instance.status = data.get('status')
        instance.save()

        instance = self.get_next_billing_date(instance)

        return instance

    def get_next_billing_date(self, instance: Subscription):
        try:
            response = stripe.Invoice.upcoming(customer=instance.user.external_id)
            next_billing_day = int_to_timestamp(response['created'])
            instance.next_billing_day = next_billing_day
            instance.save()
            return instance
        except error.InvalidRequestError as e:
            raise exceptions.StripeUpcomingInvoiceRetrieveException(e.user_message)
        except error.StripeError as e:
            raise exceptions.StripeUnhandledException(e.user_message)


class InvoiceHandler(StripeMixin):
    """
    https://stripe.com/docs/api/invoices
    """
    model = stripe.Invoice

    def update_instance(self, data, instance: Invoice) -> Invoice:
        instance.external_id = data['id']
        instance.number = data['number']
        instance.collection_method = data['collection_method']
        instance.currency = Currency.objects.get(code__iexact=data['currency'])

        try:
            instance.user = User.objects.get(external_id=data['customer'])
        except User.DoesNotExist:
            raise exceptions.StripeObjectNotFound(_('Customer not found'))

        instance.customer_internal_id = data['customer']

        try:
            instance.subscription = Subscription.objects.get(external_id=data['subscription'])
        except Subscription.DoesNotExist:
            instance.subscription = None

        instance.status = data['status']
        instance.total = Decimal(data['total'] / 100)

        return instance


class PaymentHandler(StripeMixin):
    """
    https://stripe.com/docs/api/payment_intents
    """
    model = stripe.PaymentIntent

    def update_instance(self, data, instance: Payment) -> Payment:
        instance.external_id = data['id']

        try:
            instance.invoice = Invoice.objects.get(external_id=data['invoice'])
        except Invoice.DoesNotExist:
            raise exceptions.StripeObjectNotFound(_('Customer not found'))

        try:
            instance.user = User.objects.get(external_id=data['customer'])
        except User.DoesNotExist:
            raise exceptions.StripeObjectNotFound(_('Customer not found'))

        instance.currency = Currency.objects.get(code__iexact=data['currency'])
        instance.collection_method = data['status']

        return instance
