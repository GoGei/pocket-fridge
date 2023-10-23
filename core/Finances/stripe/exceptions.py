class StripeException(Exception):
    pass


class StripeUnhandledException(StripeException):
    pass


class StripeObjectIsIntegrated(StripeUnhandledException):
    pass


class StripeObjectCreateException(StripeUnhandledException):
    pass


class StripeObjectUpdateException(StripeUnhandledException):
    pass


class StripeObjectIsNotIntegrated(StripeUnhandledException):
    pass


class StripeObjectCannotDeleteException(StripeUnhandledException):
    pass


class StripeObjectNotFound(StripeUnhandledException):
    pass


class StripeGetOrCreateException(StripeUnhandledException):
    pass


class StripeInvalidListParamsException(StripeUnhandledException):
    pass


class StripeInvalidSearchException(StripeUnhandledException):
    pass


class StripeUpcomingInvoiceRetrieveException(StripeUnhandledException):
    pass


class StripePaymentMethodCreateException(StripeUnhandledException):
    pass


class StripePaymentMethodDataInvalidException(StripeUnhandledException):
    pass


class StripePaymentMethodAttachError(StripeUnhandledException):
    pass


class StripePaymentMethodDetachError(StripeUnhandledException):
    pass


class StripePaymentMethodSetDefaultException(StripeUnhandledException):
    pass
