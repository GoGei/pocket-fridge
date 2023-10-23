import django_tables2 as tables
from core.Finances.models import Product


class ProductTable(tables.Table):
    is_active = tables.BooleanColumn(orderable=True, order_by=('-archived_stamp',))
    actions = tables.TemplateColumn(orderable=False, attrs={"td": {"style": "width: 15%"}},
                                    template_name='Manager/Stripe/Product/product_table_actions.html')

    class Meta:
        model = Product
        template_name = "django_tables2/bootstrap4.html"
        fields = (
            'id',
            'name',
            'external_id',
            'is_default',
            'is_active',
            'actions',
        )
        attrs = {"class": "table table-hover"}
