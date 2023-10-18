import django_filters
from django.utils.translation import ugettext as _

from core.Finances.models import Invoice
from core.Utils.filter_fields import SearchFilterField


class InvoiceFilterForm(django_filters.FilterSet):
    search = SearchFilterField()
    status = django_filters.ChoiceFilter(label=_('Status'), method='status_filter',
                                         choices=Invoice.InvoiceStatusChoices.choices)

    def search_qs(self, queryset, name, value):
        return SearchFilterField.search_qs(queryset, name, value,
                                           search_fields=('number', 'external_id', 'customer_internal_id'))

    def status_filter(self, queryset, name, value):
        if value:
            queryset = queryset.filter(status=value)
        return queryset
