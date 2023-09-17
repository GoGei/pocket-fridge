import django_filters
from django.utils.translation import ugettext as _
from core.Utils.filter_fields import SearchFilterField, IsActiveFilterField, IsFilledFilterForm


class UserFilterForm(django_filters.FilterSet):
    search = SearchFilterField()
    is_active = IsActiveFilterField()
    is_email_filled = IsFilledFilterForm(label=_('Is email filled'),
                                         method='is_email_filled_filter')
    is_name_filled = IsFilledFilterForm(label=_('Is name filled'),
                                        method='is_name_filled_filter')

    def is_active_filter(self, queryset, name, value):
        return IsActiveFilterField.is_active_filter(queryset, name, value,
                                                    activity_field='is_active')

    def search_qs(self, queryset, name, value):
        return SearchFilterField.search_qs(queryset, name, value,
                                           search_fields=('first_name', 'last_name', 'email'))

    def is_email_filled_filter(self, queryset, name, value):
        return IsFilledFilterForm.is_filled_filter(queryset, name, value,
                                                   fields='email')

    def is_name_filled_filter(self, queryset, name, value):
        return IsFilledFilterForm.is_filled_filter(queryset, name, value,
                                                   fields=('first_name', 'last_name'))
