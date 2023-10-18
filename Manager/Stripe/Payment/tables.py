import django_tables2 as tables
from core.Finances.models import Payment


class PaymentTable(tables.Table):
    invoice = tables.TemplateColumn(orderable=False, attrs={"td": {"style": "width: 15%"}},
                                    template_name='Manager/Stripe/Payment/payment_table_invoice.html')
    actions = tables.TemplateColumn(orderable=False, attrs={"td": {"style": "width: 15%"}},
                                    template_name='Manager/Stripe/Payment/payment_table_actions.html')

    class Meta:
        model = Payment
        template_name = "django_tables2/bootstrap4.html"
        fields = (
            'id',
            'invoice',
            'status',
            'actions',
        )
        attrs = {"class": "table table-hover"}
