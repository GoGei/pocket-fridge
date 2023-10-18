import django_filters
from django.utils.translation import ugettext as _

from core.Finances.models import Payment
from core.Utils.filter_fields import SearchFilterField


class PaymentFilterForm(django_filters.FilterSet):
    search = SearchFilterField()
    status = django_filters.ChoiceFilter(label=_('Status'), method='status_filter',
                                         choices=Payment.PaymentIntentStatusChoices.choices)

    def search_qs(self, queryset, name, value):
        return SearchFilterField.search_qs(queryset, name, value,
                                           search_fields=('invoice__number', 'invoice__external_id', 'external_id'))

    def status_filter(self, queryset, name, value):
        if value:
            queryset = queryset.filter(status=value)
        return queryset
