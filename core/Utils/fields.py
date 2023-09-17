from django import forms
from core.Utils.validators import (
    PhoneValidator, UppercaseValidator, LowercaseValidator, SpecialValidator, DigitsValidator
)


class PhoneField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(PhoneField, self).__init__(*args, **kwargs)
        self.validators.append(PhoneValidator)


class PasswordField(forms.CharField):
    def __init__(self, with_uppercase=True, with_lowercase=True, with_special=True, with_digits=True, widget_attrs=None,
                 *args, **kwargs):
        kwargs.setdefault('widget', forms.PasswordInput(attrs=widget_attrs or {"data-toggle": "password"}))
        kwargs.setdefault('min_length', 8)
        kwargs.setdefault('max_length', 24)

        super(PasswordField, self).__init__(*args, **kwargs)

        if with_uppercase:
            self.validators.append(UppercaseValidator())
        if with_lowercase:
            self.validators.append(LowercaseValidator())
        if with_special:
            self.validators.append(SpecialValidator())
        if with_digits:
            self.validators.append(DigitsValidator())
