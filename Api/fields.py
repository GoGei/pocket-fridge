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


class ActivePrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return super().get_queryset().active()


class UserPrimaryKeyRelatedField(ActivePrimaryKeyRelatedField):
    def __init__(self, **kwargs):
        self.filter_field = kwargs.pop('filter_field', 'user')
        super().__init__(**kwargs)

    def get_user(self):
        return self.context.get('user')

    def get_queryset(self):
        queryset = super().get_queryset()
        _filter = {self.filter_field: self.get_user()}
        queryset = queryset.filter(**_filter)
        return queryset


class FridgePrimaryKeyRelatedField(ActivePrimaryKeyRelatedField):
    def __init__(self, **kwargs):
        self.filter_field = kwargs.pop('filter_field', 'fridge')
        super().__init__(**kwargs)

    def get_fridge(self):
        return self.context.get('fridge')

    def get_queryset(self):
        queryset = super().get_queryset()
        _filter = {self.filter_field: self.get_fridge()}
        queryset = queryset.filter(**_filter)
        return queryset
