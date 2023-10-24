from decimal import Decimal

import pytz
import stripe
from django.db import transaction
from stripe import error
from datetime import datetime
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from . import exceptions
from .mixins import StripeMixin

from core.Finances.models import Product, Price, Subscription, Invoice, Payment, PaymentMethod
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
            'active': instance.is_active(),
            'description': instance.description or '',
            'metadata': {
                'is_default': instance.is_default,
            }
        }
        return response

    def update_instance(self, data, instance: Product = None) -> Product:
        try:
            instance = Product.objects.get(external_id=data['id'])
        except Product.DoesNotExist:
            if instance:
                instance.external_id = data['id']
            else:
                instance = Product(external_id=data['id'])

        instance.name = data['name']
        instance.description = data['description']
        instance.save()

        metadata = data.get('metadata', {})
        is_default = metadata.get('is_default', False)
        if is_default:
            instance.set_as_default()

        active = data['active']
        if not active:
            instance.is_published = False
            instance.archive()
        elif active and not instance.is_active():
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
            'active': instance.is_active(),
            'recurring': instance.recurring,
            'unit_amount_decimal': instance.stripify_price,
            'metadata': {
                'is_default': instance.is_default,
            }
        }

        return response

    def update_instance(self, data, instance: Price = None) -> Price:
        try:
            instance = Price.objects.get(external_id=data['id'])
        except Price.DoesNotExist:
            if instance:
                instance.external_id = data['id']
            else:
                instance = Price(external_id=data['id'])

        instance.currency = Currency.objects.get(code__iexact=data['currency'])
        instance.product = Product.objects.get(external_id=data['product'])
        recurring = data['recurring']
        instance.interval = recurring['interval']
        instance.interval_count = recurring['interval_count']
        instance.usage_type = recurring['usage_type']
        instance.price = Price.unstripify_price(data['unit_amount_decimal'])
        instance.save()

        active = data['active']
        if not active:
            instance.archive()
        elif active and not instance.is_active():
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

    def update_instance(self, data, instance: Subscription = None) -> Subscription:
        try:
            instance = Subscription.objects.get(external_id=data['id'])
        except Subscription.DoesNotExist:
            if instance:
                instance.external_id = data['id']
            else:
                instance = Subscription(external_id=data['id'])

        item_data = data['items']['data'][0]
        price_data = item_data['price']

        try:
            instance.product = Product.objects.get(external_id=price_data['product'])
        except Product.DoesNotExist:
            raise exceptions.StripeObjectNotFound(_('Product not found'))

        try:
            instance.price = Price.objects.get(external_id=price_data['id'])
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

    def update_instance(self, data, instance: Invoice = None) -> Invoice:
        try:
            instance = Invoice.objects.get(external_id=data['id'])
        except Invoice.DoesNotExist:
            if instance:
                instance.external_id = data['id']
            else:
                instance = Invoice(external_id=data['id'])

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

    def update_instance(self, data, instance: Payment = None) -> Payment:
        try:
            instance = Payment.objects.get(external_id=data['id'])
        except Payment.DoesNotExist:
            if instance:
                instance.external_id = data['id']
            else:
                instance = Payment(external_id=data['id'])

        try:
            instance.invoice = Invoice.objects.get(external_id=data['invoice'])
        except Invoice.DoesNotExist:
            raise exceptions.StripeObjectNotFound(_('Invoice not found'))

        try:
            instance.user = User.objects.get(external_id=data['customer'])
        except User.DoesNotExist:
            raise exceptions.StripeObjectNotFound(_('Customer not found'))

        instance.currency = Currency.objects.get(code__iexact=data['currency'])
        instance.collection_method = data['status']

        return instance


class CustomerHandler(StripeMixin):
    """
    https://stripe.com/docs/api/customers
    """
    model = stripe.Customer

    def instance_to_stripe(self, instance: User) -> dict:
        response = {
            'description': f'Customer instance of user {instance.id}',
            'name': instance.email,
        }
        return response

    def update_instance(self, data, instance: User = None) -> Subscription:
        try:
            instance = User.objects.get(external_id=data['id'])
        except User.DoesNotExist:
            if instance:
                instance.external_id = data['id']
            else:
                instance = User.objects.get(email__iexact=data['name'])

        instance.external_id = data['id']
        instance.save()

        return instance

    @transaction.atomic
    def set_as_default_payment_method(self, payment_method: PaymentMethod):
        data = {'invoice_settings': {'default_payment_method': payment_method.external_id}}
        try:
            response = self.model.modify(payment_method.user.external_id, **data)
            payment_method.is_default = True
            payment_method.save()
        except error.InvalidRequestError as e:
            raise exceptions.StripePaymentMethodSetDefaultException(e.user_message)
        except error.StripeError as e:
            raise exceptions.StripeUnhandledException(e.user_message)

        return response


class PaymentMethodHandler(StripeMixin):
    model = stripe.PaymentMethod

    def update_instance(self, data, user: User, instance: PaymentMethod = None):
        try:
            instance = PaymentMethod.objects.get(external_id=data['id'])
        except PaymentMethod.DoesNotExist:
            if instance:
                instance.external_id = data['id']
            else:
                instance = PaymentMethod(external_id=data['id'])
        instance.user = user

        card_data = data['card']
        instance.expire_date = PaymentMethod.form_expire_date_to_model(card_data)
        instance.last_digits_of_card = card_data['last4']
        instance.card_type = card_data['brand']

        instance.save()
        return instance

    def update_token_instance(self, data, user: User, instance: PaymentMethod = None):
        try:
            instance = PaymentMethod.objects.get(external_id=data['id'])
        except PaymentMethod.DoesNotExist:
            if instance:
                instance.external_id = data['id']
            else:
                instance = PaymentMethod(external_id=data['id'])
        instance.user = user

        card_data = data['card']
        instance.expire_date = PaymentMethod.form_expire_date_to_model(card_data)
        instance.last_digits_of_card = card_data['last4']
        instance.card_type = card_data['brand']

        instance.save()
        return instance

    @transaction.atomic
    def create(self, card_data, user, instance: PaymentMethod = None):
        try:
            response = self.model.create(type='card', card=card_data)
            instance = self.update_instance(response, user, instance)
        except error.InvalidRequestError as e:
            raise exceptions.StripePaymentMethodCreateException(e.user_message)
        except error.CardError as e:
            raise exceptions.StripePaymentMethodDataInvalidException(e.user_message)
        except error.StripeError as e:
            raise exceptions.StripeUnhandledException(e.user_message)

        return instance

    @transaction.atomic
    def create_token(self, card_data, user, instance: PaymentMethod = None):
        try:
            response = stripe.Token.create(card=card_data)
            instance = self.update_token_instance(response, user, instance)
        except error.InvalidRequestError as e:
            raise exceptions.StripePaymentMethodCreateException(e.user_message)
        except error.CardError as e:
            raise exceptions.StripePaymentMethodDataInvalidException(e.user_message)
        except error.StripeError as e:
            raise exceptions.StripeUnhandledException(e.user_message)

        return instance

    def attach_to_customer(self, card):
        try:
            response = self.model.attach(card.external_id, customer=card.user.external_id)
        except error.InvalidRequestError as e:
            raise exceptions.StripePaymentMethodAttachError(e.user_message)
        except error.CardError as e:
            raise exceptions.StripePaymentMethodDataInvalidException(e.user_message)
        except error.StripeError as e:
            raise exceptions.StripeUnhandledException(e.user_message)

        return response

    def detach_from_customer(self, card):
        try:
            response = self.model.detach(card.external_id)
        except error.InvalidRequestError as e:
            raise exceptions.StripePaymentMethodDetachError(e.user_message)
        except error.StripeError as e:
            raise exceptions.StripeUnhandledException(e.user_message)

        return response
