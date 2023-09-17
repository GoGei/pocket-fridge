from django.conf import settings
from django.contrib.auth import login
from django.forms import model_to_dict
from django_hosts import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext as _
from django.contrib import messages

from core.Utils.Access.decorators import manager_required, superuser_required
from core.User.models import User
from .forms import AdminFilterForm, AdminFormAdd, AdminFormEdit, AdminSetPasswordForm, AdminResetPasswordForm
from .tables import AdminTable


@manager_required
def admins_list(request):
    qs = User.objects.admins().order_by('email')

    filter_form = AdminFilterForm(request.GET, queryset=qs, request=request)
    qs = filter_form.qs

    table_body = AdminTable(qs, request=request)
    page = request.GET.get("page", 1)
    table_body.paginate(page=page, per_page=settings.ITEMS_PER_PAGE)

    table = {
        'body': table_body,
        'filter': {
            'title': _('Admin filter'),
            'body': filter_form,
            'action': reverse('manager-admins-list', host='manager')
        }
    }
    return render(request, 'Manager/Admins/admins_list.html',
                  {'table': table})


@manager_required
def admins_view(request, admin_id):
    admin = get_object_or_404(User.objects.admins(), pk=admin_id)
    return render(request, 'Manager/Admins/admins_view.html', {'admin': admin})


@superuser_required
def admins_add(request):
    form_body = AdminFormAdd(request.POST or None)

    if '_cancel' in request.POST:
        return redirect(reverse('manager-admins-list', host='manager'))

    if form_body.is_valid():
        admin = form_body.save()
        messages.success(request, _(f'Admin {admin.email} was successfully created'))
        # return redirect(reverse('manager-admins-list', host='manager'))
        return redirect(reverse('manager-admins-set-password', args=[admin.id], host='manager'))

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True},
        'title': _('Add admin'),
        'description': _('Please, fill in the form below to add an admin'),
    }

    return render(request, 'Manager/Admins/admins_add.html', {'form': form})


@manager_required
def admins_reset_password(request):
    admin = request.user
    form_body = AdminResetPasswordForm(request.POST or None, admin=admin)

    if '_cancel' in request.POST:
        return redirect(reverse('manager-index', host='manager'))

    if form_body.is_valid():
        form_body.save()
        messages.success(request, _('Your password was successfully set'))
        login(request, admin)
        return redirect(reverse('manager-index', host='manager'))

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True},
        'title': _('Reset password'),
        'description': _('Please, fill in the form below to set new password'),
    }

    return render(request, 'Manager/Admins/admins_reset_password.html', {'form': form,
                                                                         'admin': admin})


@superuser_required
def admins_edit(request, admin_id):
    admin = get_object_or_404(User.objects.admins(), pk=admin_id)

    if '_cancel' in request.POST:
        return redirect(reverse('manager-admins-view', args=[admin_id], host='manager'))

    initial = model_to_dict(admin)
    initial['status'] = AdminFormEdit.to_status(admin)
    form_body = AdminFormEdit(request.POST or None, instance=admin, initial=initial)
    if form_body.is_valid():
        admin = form_body.save()
        messages.success(request, _(f'Admin {admin.email} was successfully edited'))
        return redirect(reverse('manager-admins-view', args=[admin_id], host='manager'))

    form = {
        'body': form_body,
        'buttons': {'submit': True, 'cancel': True},
        'title': _('Edit admin'),
        'description': _('Please, fill in the form below to edit an admin'),
    }

    return render(request, 'Manager/Admins/admins_edit.html', {'form': form,
                                                               'admin': admin})


@superuser_required
def admins_set_password(request, admin_id):
    admin = get_object_or_404(User.objects.admins(), pk=admin_id)
    form_body = AdminSetPasswordForm(request.POST or None, admin=admin)

    if '_cancel' in request.POST:
        return redirect(reverse('manager-admins-view', args=[admin_id], host='manager'))

    if form_body.is_valid():
        form_body.save()
        messages.success(request, _(f'Admin {admin.email}\'s password was successfully set'))
        return redirect(reverse('manager-admins-list', host='manager'))

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True},
        'title': _('Set admin password'),
        'description': _('Please, fill in the form below to set password for an admin'),
    }

    return render(request, 'Manager/Admins/admins_set_password.html', {'form': form,
                                                                       'admin': admin})
