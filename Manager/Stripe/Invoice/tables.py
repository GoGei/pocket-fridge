import django_tables2 as tables
from core.Finances.models import Invoice


class InvoiceTable(tables.Table):
    actions = tables.TemplateColumn(orderable=False, attrs={"td": {"style": "width: 15%"}},
                                    template_name='Manager/Stripe/Invoice/invoice_table_actions.html')

    class Meta:
        model = Invoice
        template_name = "django_tables2/bootstrap4.html"
        fields = (
            'id',
            'number',
            'customer_internal_id',
            'status',
            'total',
            'actions',
        )
        attrs = {"class": "table table-hover"}
