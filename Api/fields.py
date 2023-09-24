from rest_framework import serializers
from Api.validators import user_password_validators


class UserPasswordField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs.setdefault('min_length', 8)
        kwargs.setdefault('max_length', 20)
        kwargs.setdefault('write_only', True)
        kwargs.setdefault('required', True)

        super().__init__(**kwargs)
        for validator in user_password_validators:
            self.validators.append(validator())

    def to_internal_value(self, data):
        data = data.strip()
        data = data.replace(' ', '')
        data = super(UserPasswordField, self).to_internal_value(data)
        return data
