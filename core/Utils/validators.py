from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

PhoneValidator = RegexValidator(regex=r'^([+]?[\s0-9]+)?(\d{3}|[(]?[0-9]+[)])?([-]?[\s]?[0-9])+$',
                                message=(
                                    "Phone number must be entered in the format: '+380(99)-999-9999'."))


class UppercaseValidator:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, value):
        # def UppercaseValidator(value):
        if not any(char.isupper() for char in value):
            raise ValidationError(_("Value does not contains uppercase letters"))


class LowercaseValidator:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, value):
        # def LowercaseValidator(value):
        if not any(char.islower() for char in value):
            raise ValidationError(_("Value does not contains lowercase letters"))


class SpecialValidator:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, value):
        # def SpecialValidator(value):
        chars = '!@._'
        if not any(char in chars for char in value):
            raise ValidationError(_("Value does not contains special characters"))


class DigitsValidator:
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, value):
        # def DigitsValidator(value):
        if not any(char.isdigit() for char in value):
            raise ValidationError(_("Value does not contains digits"))
