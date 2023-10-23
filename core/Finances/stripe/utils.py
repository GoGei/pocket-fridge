from . import exceptions
from .handlers import InvoiceHandler, PaymentHandler


def load_invoices(raise_errors=True):
    handler = InvoiceHandler()
    __load_instances(handler, raise_errors)


def load_payments(raise_errors=True):
    handler = PaymentHandler()
    __load_instances(handler, raise_errors)


def __load_instances(handler, raise_errors=True):
    response = handler.list()
    ids = [item['id'] for item in response['data']]
    for _id in ids:
        try:
            handler.get_or_create(external_id=_id)
        except exceptions.StripeException as e:
            if raise_errors:
                raise exceptions.StripeException(e)
            else:
                print('[!] something went wrong: %s' % e)
