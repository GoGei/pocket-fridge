"""
Fields designed to use them in django_filter sets
Due to the unavailability of django_filter to access field directly it can be implemented the following:
    Provide preconfigured field
    Provide filter to call it in mentioned function
"""
import django_filters
from django import forms
from django.db.models import Q
from django.utils.translation import ugettext as _


class SearchFilterField(django_filters.CharFilter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _('Search'))
        kwargs.setdefault('method', 'search_qs')
        kwargs.setdefault('widget', self.get_default_widget())
        super().__init__(*args, **kwargs)

    @classmethod
    def get_default_widget(cls):
        return forms.TextInput(attrs={'type': 'search', 'class': 'form-control', 'placeholder': _('Search')})

    @classmethod
    def search_qs(cls, queryset, name, value, search_fields=()):
        _filter = Q()
        for field in search_fields:
            _filter |= Q(**{f'{field}__icontains': value})
        queryset = queryset.filter(_filter)
        return queryset


class IsActiveFilterField(django_filters.BooleanFilter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _('Is active'))
        kwargs.setdefault('method', 'is_active_filter')
        kwargs.setdefault('widget', self.get_default_widget())
        super().__init__(*args, **kwargs)

    @classmethod
    def get_default_widget(cls):
        choices = [(None, _('Select')), (True, _('Active')), (False, _('Not active'))]
        return forms.Select(attrs={'class': 'form-control'},
                            choices=choices)

    @classmethod
    def is_active_filter(cls, queryset, name, value, activity_field=None):
        if isinstance(value, bool):
            if activity_field:
                _filter = {activity_field: value}
            else:
                # CrmMixin field
                if value is True:
                    _filter = {'archived_stamp__isnull': True}
                else:
                    _filter = {'archived_stamp__isnull': False}
            queryset = queryset.filter(**_filter)
        return queryset


class IsFilledFilterForm(django_filters.BooleanFilter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label', _('Is filled'))
        kwargs.setdefault('method', 'is_filled_filter')
        kwargs.setdefault('widget', self.get_default_widget())
        super().__init__(*args, **kwargs)

    @classmethod
    def get_default_widget(cls):
        choices = [(None, _('Select')), (True, _('Filled')), (False, _('Not filled'))]
        return forms.Select(attrs={'class': 'form-control'},
                            choices=choices)

    @classmethod
    def is_filled_filter(cls, queryset, name, value, fields=None):
        if isinstance(value, bool):
            if isinstance(fields, str):
                fields = (fields,)

            if value is True:
                _filter = {f'{field}__isnull': False for field in fields}
            else:
                _filter = {f'{field}__isnull': True for field in fields}
            queryset = queryset.filter(**_filter)
        return queryset
