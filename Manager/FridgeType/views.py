import json

from django.core.management import call_command
from django.http import HttpResponse
from django_hosts import reverse
from django.conf import settings
from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext as _, ungettext_lazy
from django.contrib import messages
from rest_framework.renderers import JSONRenderer

from core.Fridge.models import FridgeType
from core.Fridge.constants import FRIDGE_TYPE_DEFAULT_FIXTURE_PATH
from core.Utils.Access.decorators import manager_required, superuser_required
from core.Utils.Exporter.exporter import CrmMixinJSONExporter
from .forms import FridgeTypeFilterForm, FridgeTypeFormAdd, FridgeTypeFormEdit, FridgeTypeImportForm
from .tables import FridgeTypeTable
import logging

logger = logging.getLogger(__name__)


@manager_required
def fridge_type_list(request):
    qs = FridgeType.objects.all().order_by('name')

    filter_form = FridgeTypeFilterForm(request.GET, queryset=qs, request=request)
    qs = filter_form.qs

    table_body = FridgeTypeTable(qs, request=request)
    page = request.GET.get("page", 1)
    table_body.paginate(page=page, per_page=settings.ITEMS_PER_PAGE)

    table = {
        'body': table_body,
        'filter': {
            'title': _('Fridge type filter'),
            'body': filter_form,
            'action': reverse('manager-fridge-type-list', host='manager')
        }
    }
    return render(request, 'Manager/FridgeType/fridge_type_list.html',
                  {'table': table})


@manager_required
def fridge_type_view(request, fridge_type_id):
    fridge_type = get_object_or_404(FridgeType, pk=fridge_type_id)
    return render(request, 'Manager/FridgeType/fridge_type_view.html', {'fridge_type': fridge_type})


@manager_required
def fridge_type_add(request):
    form_body = FridgeTypeFormAdd(request.POST or None)

    if '_cancel' in request.POST:
        return redirect(reverse('manager-fridge-type-list', host='manager'))

    if form_body.is_valid():
        fridge_type = form_body.save()
        msg = _(f'Fridge type {fridge_type.label} was successfully created')
        messages.success(request, msg)
        logger.info(msg)

        return redirect(reverse('manager-fridge-type-list', host='manager'))

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True},
        'title': _('Add fridge type'),
        'description': _('Please, fill in the form below to add fridge type'),
    }

    return render(request, 'Manager/FridgeType/fridge_type_add.html', {'form': form})


@manager_required
def fridge_type_edit(request, fridge_type_id):
    fridge_type = get_object_or_404(FridgeType, pk=fridge_type_id)

    if '_cancel' in request.POST:
        return redirect(reverse('manager-fridge-type-view', args=[fridge_type_id], host='manager'))

    initial = model_to_dict(fridge_type)
    form_body = FridgeTypeFormEdit(request.POST or None, instance=fridge_type, initial=initial)
    if form_body.is_valid():
        fridge_type = form_body.save()
        msg = _(f'Fridge type {fridge_type.label} was successfully edited')
        messages.success(request, msg)
        logger.info(msg)

        return redirect(reverse('manager-fridge-type-view', args=[fridge_type_id], host='manager'))

    form = {
        'body': form_body,
        'buttons': {'submit': True, 'cancel': True},
        'title': _('Edit Fridge type'),
        'description': _('Please, fill in the form below to edit a fridge type'),
    }

    return render(request, 'Manager/FridgeType/fridge_type_edit.html', {'form': form,
                                                                        'fridge_type': fridge_type})


@manager_required
def fridge_type_archive(request, fridge_type_id):
    fridge_type = get_object_or_404(FridgeType.objects.prefetch_related('fridge_set'), pk=fridge_type_id)

    categories = fridge_type.fridge_set.all()
    if categories.exists():
        msg = ungettext_lazy('This fridge type is used in fridge %s time!',
                             'This fridge type is used in fridges %s times!') % categories.count()
        messages.warning(request, msg)
        logger.info(msg)
    else:
        fridge_type.archive(request.user)
        msg = _(f'Fridge type {fridge_type.label} was successfully archived')
        messages.success(request, msg)
        logger.info(msg)

    return redirect(reverse('manager-fridge-type-list', host='manager'))


@manager_required
def fridge_type_restore(request, fridge_type_id):
    fridge_type = get_object_or_404(FridgeType, pk=fridge_type_id)
    fridge_type.restore(request.user)
    msg = _(f'Fridge type {fridge_type.label} was successfully restored')
    messages.success(request, msg)
    logger.info(msg)

    return redirect(reverse('manager-fridge-type-list', host='manager'))


@superuser_required
def fridge_type_view_fixture(request):
    with open(FRIDGE_TYPE_DEFAULT_FIXTURE_PATH, 'r') as f:
        data = json.load(f)
    return render(request, 'Manager/FridgeType/fridge_type_view_fixture.html', {'data': data})


@superuser_required
def fridge_type_load_fixture(request):
    form_body = FridgeTypeImportForm(request.POST or None,
                                     request.FILES or None)

    if '_cancel' in request.POST:
        return redirect(reverse('manager-fridge-type-list', host='manager'))

    if form_body.is_valid():
        try:
            items, created_count = form_body.load()
            msg = _(f'Fridge type {created_count} was successfully created')
            messages.success(request, msg)
            logger.info(msg)

            msg = _(f'Fridge type {len(items)} was successfully updated')
            messages.success(request, msg)
            logger.info(msg)

            return redirect(reverse('manager-fridge-type-list', host='manager'))
        except ValueError as e:
            form_body.add_error('file', str(e))

    form = {
        'body': form_body,
        'buttons': {'submit': True, 'cancel': True},
        'title': _('Load fridge type'),
    }

    return render(request, 'Manager/FridgeType/fridge_type_load_fixture.html', {'form': form})


@manager_required
def fridge_type_export_to_fixture(request):
    data = CrmMixinJSONExporter(model=FridgeType, export_fields=('name', 'slug')).export()
    content = JSONRenderer().render(data)

    response = HttpResponse(content, content_type='application/json')
    filename = 'fridge_types.json'
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    response['Cache-Control'] = 'no-cache'
    return response


@superuser_required
def fridge_type_load_default_fixture(request):
    call_command('load_fridge_type_fixture')
    msg = _('Fridge type default fixture was successfully loaded')
    messages.success(request, msg)
    logger.info(msg)

    return redirect(reverse('manager-fridge-type-list', host='manager'))
