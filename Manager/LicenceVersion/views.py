from django_hosts import reverse
from django.conf import settings
from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext as _
from django.contrib import messages

from core.Licence.models import LicenceVersion, PrivacyPolicy, TermsOfUse
from core.Utils.Access.decorators import manager_required
from .forms import LicenceVersionFilterForm, LicenceVersionFormAdd, LicenceVersionFormEdit
from .tables import LicenceVersionTable


@manager_required
def licence_version_list(request):
    qs = LicenceVersion.objects.all().order_by('name')

    filter_form = LicenceVersionFilterForm(request.GET, queryset=qs, request=request)
    qs = filter_form.qs

    table_body = LicenceVersionTable(qs, request=request)
    page = request.GET.get("page", 1)
    table_body.paginate(page=page, per_page=settings.ITEMS_PER_PAGE)

    table = {
        'body': table_body,
        'filter': {
            'title': _('Licence version filter'),
            'body': filter_form,
            'action': reverse('manager-licence-version-list', host='manager')
        }
    }
    return render(request, 'Manager/LicenceVersion/licence_version_list.html',
                  {'table': table})


@manager_required
def licence_version_view(request, licence_version_id):
    licence_version = get_object_or_404(LicenceVersion, pk=licence_version_id)
    privacy_policy = PrivacyPolicy.get_default(licence_version)
    terms_of_use = TermsOfUse.get_default(licence_version)
    return render(request, 'Manager/LicenceVersion/licence_version_view.html',
                  {'licence_version': licence_version,
                   'privacy_policy': privacy_policy,
                   'terms_of_use': terms_of_use,
                   })


@manager_required
def licence_version_add(request):
    form_body = LicenceVersionFormAdd(request.POST or None, request.FILES or None)

    if '_cancel' in request.POST:
        return redirect(reverse('manager-licence-version-list', host='manager'))

    if form_body.is_valid():
        licence_version = form_body.save()
        messages.success(request, _(f'Licence version {licence_version.label} was successfully created'))
        return redirect(reverse('manager-licence-version-list', host='manager'))

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True},
        'title': _('Add Licence version'),
        'description': _('Please, fill in the form below to add Licence version'),
    }

    return render(request, 'Manager/LicenceVersion/licence_version_add.html', {'form': form})


@manager_required
def licence_version_edit(request, licence_version_id):
    licence_version = get_object_or_404(LicenceVersion, pk=licence_version_id)

    if '_cancel' in request.POST:
        return redirect(reverse('manager-licence-version-view', args=[licence_version_id], host='manager'))

    initial = model_to_dict(licence_version)
    form_body = LicenceVersionFormEdit(request.POST or None, request.FILES or None,
                                       instance=licence_version, initial=initial)
    if form_body.is_valid():
        licence_version = form_body.save()
        messages.success(request, _(f'Licence version {licence_version.label} was successfully edited'))
        return redirect(reverse('manager-licence-version-view', args=[licence_version_id], host='manager'))

    form = {
        'body': form_body,
        'buttons': {'submit': True, 'cancel': True},
        'title': _('Edit Licence version'),
        'description': _('Please, fill in the form below to edit a Licence version'),
    }

    return render(request, 'Manager/LicenceVersion/licence_version_edit.html', {'form': form,
                                                                                'licence_version': licence_version})


@manager_required
def licence_version_archive(request, licence_version_id):
    licence_version = get_object_or_404(LicenceVersion.objects.prefetch_related('fridge_set'), pk=licence_version_id)
    licence_version.archive(request.user)
    messages.success(request, _(f'Licence version {licence_version.label} was successfully archived'))
    return redirect(reverse('manager-licence-version-list', host='manager'))


@manager_required
def licence_version_restore(request, licence_version_id):
    licence_version = get_object_or_404(LicenceVersion, pk=licence_version_id)
    licence_version.restore(request.user)
    messages.success(request, _(f'Licence version {licence_version.label} was successfully restored'))
    return redirect(reverse('manager-licence-version-list', host='manager'))


@manager_required
def licence_version_set_default(request, licence_version_id):
    licence_version = get_object_or_404(LicenceVersion, pk=licence_version_id)
    licence_version.set_default()
    licence_version.modify(request.user)
    messages.success(request, _(f'Licence version {licence_version.label} was successfully set as default'))
    return redirect(reverse('manager-licence-version-list', host='manager'))
