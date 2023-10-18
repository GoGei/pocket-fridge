class StripeException(Exception):
    pass


class StripeUnhandledException(StripeException):
    pass


class StripeObjectIsIntegrated(StripeUnhandledException):
    pass


class StripeObjectCreateException(StripeUnhandledException):
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
