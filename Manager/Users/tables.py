import django_tables2 as tables
from core.User.models import User


class UserTable(tables.Table):
    name = tables.TemplateColumn(orderable=True, order_by=('first_name', 'last_name'),
                                 template_name='Manager/Users/users_table_name_field.html')
    actions = tables.TemplateColumn(orderable=False, attrs={"td": {"style": "width: 15%"}},
                                    template_name='Manager/Users/users_table_actions.html', )

    class Meta:
        model = User
        template_name = "django_tables2/bootstrap4.html"
        fields = (
            'id',
            'name',
            'email',
            'is_active',
        )
        attrs = {"class": "table table-hover"}
