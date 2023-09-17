import django_tables2 as tables
from core.Fridge.models import FridgeType


class FridgeTypeTable(tables.Table):
    is_active = tables.BooleanColumn(orderable=True, order_by=('-archived_stamp',))
    actions = tables.TemplateColumn(orderable=False, attrs={"td": {"style": "width: 15%"}},
                                    template_name='Manager/FridgeType/fridge_type_table_actions.html')

    class Meta:
        model = FridgeType
        template_name = "django_tables2/bootstrap4.html"
        fields = (
            'id',
            'name',
            'slug',
            'is_active',
            'actions',
        )
        attrs = {"class": "table table-hover"}
