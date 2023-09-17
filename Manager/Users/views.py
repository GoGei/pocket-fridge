from django.conf import settings
from django_hosts import reverse
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext as _

from core.Utils.Access.decorators import manager_required
from core.User.models import User
from .forms import UserFilterForm
from .tables import UserTable


@manager_required
def users_list(request):
    qs = User.objects.users().order_by('is_active', 'id')

    filter_form = UserFilterForm(request.GET, queryset=qs, request=request)
    qs = filter_form.qs

    table_body = UserTable(qs, request=request)
    page = request.GET.get("page", 1)
    table_body.paginate(page=page, per_page=settings.ITEMS_PER_PAGE)

    table = {
        'body': table_body,
        'filter': {
            'title': _('User filter'),
            'body': filter_form,
            'action': reverse('manager-users-list', host='manager')
        }
    }
    return render(request, 'Manager/Users/users_list.html',
                  {'table': table})


@manager_required
def users_view(request, user_id):
    user = get_object_or_404(User.objects.users(), pk=user_id)
    return render(request, 'Manager/Users/users_view.html', {'user': user})
