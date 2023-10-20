import stripe
from stripe import error
from django.conf import settings
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from . import exceptions


class StripeMixin:
    model = None

    def __init__(self):
        stripe.api_key = settings.STRIPE_API_KEY

    def instance_to_stripe(self, instance):
        """Prepare django model to stripe data"""
        raise NotImplementedError

    def update_instance(self, data, instance=None):
        """Load stripe data to instance from response"""
        raise NotImplementedError

    def list(self, *args, **kwargs):
        try:
            response = self.model.list(*args, **kwargs)
            return response
        except error.InvalidRequestError as e:
            raise exceptions.StripeInvalidListParamsException(e.user_message)
        except error.StripeError as e:
            raise exceptions.StripeUnhandledException(e.user_message)

    def search(self, query, limit=None, page=None):
        data = {'query': query}
        if limit:
            data['limit'] = limit
        if limit:
            data['page'] = page

        try:
            response = self.model.search(**data)
            return response
        except error.InvalidRequestError as e:
            raise exceptions.StripeInvalidSearchException(e.user_message)
        except error.StripeError as e:
            raise exceptions.StripeUnhandledException(e.user_message)

    def retrieve(self, instance_id):
        try:
            response = self.model.retrieve(instance_id)
            return response
        except error.InvalidRequestError as e:
            raise exceptions.StripeObjectNotFound(e.user_message)
        except error.StripeError as e:
            raise exceptions.StripeUnhandledException(e.user_message)

    @transaction.atomic
    def create(self, instance):
        stripe_data = self.instance_to_stripe(instance)
        try:
            if instance.external_id:
                raise exceptions.StripeObjectIsIntegrated(_('Object already integrated with stripe!'))

            response = self.model.create(**stripe_data)
            self.update_instance(response, instance)
        except error.InvalidRequestError as e:
            raise exceptions.StripeObjectCreateException(e.user_message)
        except error.StripeError as e:
            raise exceptions.StripeUnhandledException(e.user_message)

        return response

    @transaction.atomic
    def destroy(self, instance):
        try:
            if not instance.external_id:
                raise exceptions.StripeObjectIsNotIntegrated(_('Object is not integrated with stripe!'))

            response = self.model.delete(instance.external_id)
            return response
        except error.InvalidRequestError as e:
            raise exceptions.StripeObjectCannotDeleteException(e.user_message)
        except error.StripeError as e:
            raise exceptions.StripeUnhandledException(e.user_message)

    @transaction.atomic
    def get_or_create(self, instance=None, external_id=None):
        # if object can not be get from stripe -> create it in stripe
        try:
            if instance and not instance.external_id:
                raise exceptions.StripeObjectIsNotIntegrated(_('Object is not integrated with stripe!'))

            response = self.retrieve(external_id or instance.external_id)
            created = False
        except (exceptions.StripeObjectNotFound, exceptions.StripeObjectIsNotIntegrated):
            try:
                response = self.create(instance)
                created = True
            except (exceptions.StripeObjectCreateException, exceptions.StripeObjectIsIntegrated) as e:
                raise exceptions.StripeGetOrCreateException(e)

        return response, created

    @transaction.atomic
    def sync_from_stripe(self, instance=None, external_id=None, response=None, *args, **kwargs):
        try:
            if not (external_id or response):
                raise ValueError('Please, provide internal ID or response from stripe')

            if external_id:
                response = self.model.retrieve(external_id)

            instance = self.update_instance(data=response, instance=instance)
            instance.modify()
            return instance

        except ObjectDoesNotExist as e:
            raise exceptions.StripeObjectIsNotIntegrated(str(e))
        except error.InvalidRequestError as e:
            raise exceptions.StripeObjectNotFound(e.user_message)
        except error.StripeError as e:
            raise exceptions.StripeUnhandledException(e.user_message)
