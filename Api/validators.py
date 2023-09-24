import re
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class LengthValidator(object):
    __slots__ = ()
    message = _("The password must contain at least 8 symbols.")

    def __call__(self, password):
        if len(password) < 8:
            raise ValidationError(self.message, code='too_short')


class MaxLengthValidator(object):
    __slots__ = ()
    message = _("The password must contain at most 20 symbols.")

    def __call__(self, password):
        if len(password) > 20:
            raise ValidationError(self.message, code='too_long')


class HasLowerCaseValidator(object):
    __slots__ = ()
    message = _("The password must contain at least one lowercase character.")

    def __call__(self, password):
        if password == password.upper():
            raise ValidationError(self.message, code='missing_lower_case')


class HasUpperCaseValidator(object):
    __slots__ = ()
    message = _("The password must contain at least one uppercase character.")

    def __call__(self, password):
        if password == password.lower():
            raise ValidationError(self.message, code='missing_upper_case')


class HasNumberValidator(object):
    __slots__ = ()
    message = _("The password must contain at least one numeric character.")

    def __call__(self, password):
        if re.search('[0-9]', password) is None:
            raise ValidationError(self.message, code='missing_numeric')


class HasSymbolValidator(object):
    __slots__ = ()
    message = _("The password must contain at least one of these special symbols: !?@#$%^&*_~()- .")

    def __call__(self, password):
        if re.search('[!?@#$%^&*_~()-]', password) is None:
            raise ValidationError(self.message, code='missing_symbol')


class HasOnlyASCIISymbolValidator(object):
    __slots__ = ()
    message = _("The password must contain only latin characters.")

    def __call__(self, password):
        if ' ' in password:
            raise serializers.ValidationError(self.message)


password_validators = (
    LengthValidator,
    MaxLengthValidator,
    # HasUpperCaseValidator,
    # HasLowerCaseValidator,
    # HasNumberValidator,
    # HasSymbolValidator,
    HasOnlyASCIISymbolValidator
)

user_password_validators = (
    LengthValidator,
    MaxLengthValidator,
    # HasUpperCaseValidator,
    # HasLowerCaseValidator,
    # HasNumberValidator,
    HasOnlyASCIISymbolValidator
)
