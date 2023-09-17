import django_tables2 as tables
from core.User.models import User


class AdminTable(tables.Table):
    phone = tables.TemplateColumn(orderable=True, attrs={"td": {"style": "width: 15%"}},
                                  template_name='Manager/Admins/admins_table_phone.html')
    status = tables.TemplateColumn(orderable=True, attrs={"td": {"style": "width: 15%"}},
                                   order_by=('-is_superuser',),
                                   template_name='Manager/Admins/admins_table_manager_status.html')
    actions = tables.TemplateColumn(orderable=False, attrs={"td": {"style": "width: 15%"}},
                                    template_name='Manager/Admins/admins_table_actions.html')

    class Meta:
        model = User
        template_name = "django_tables2/bootstrap4.html"
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'status',
            'is_active',
        )
        attrs = {"class": "table table-hover"}
