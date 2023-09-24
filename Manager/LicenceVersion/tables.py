import django_tables2 as tables
from core.Licence.models import LicenceVersion


class LicenceVersionTable(tables.Table):
    is_active = tables.BooleanColumn(orderable=True, order_by=('-archived_stamp',))
    is_default = tables.BooleanColumn(orderable=True)
    actions = tables.TemplateColumn(orderable=False, attrs={"td": {"style": "width: 15%"}},
                                    template_name='Manager/LicenceVersion/licence_version_table_actions.html')

    class Meta:
        model = LicenceVersion
        template_name = "django_tables2/bootstrap4.html"
        fields = (
            'id',
            'name',
            'slug',
            'is_active',
            'is_default',
            'actions',
        )
        attrs = {"class": "table table-hover"}
