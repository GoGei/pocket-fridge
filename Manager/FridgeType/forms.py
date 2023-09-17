import json
import django_filters
from django import forms
from django.utils.translation import ugettext as _
from core.Fridge.models import FridgeType
from core.Utils.filter_fields import SearchFilterField, IsActiveFilterField
from core.Utils.Exporter.importer import CrmMixinJSONLoader


class FridgeTypeFilterForm(django_filters.FilterSet):
    search = SearchFilterField()
    is_active = IsActiveFilterField()

    def is_active_filter(self, queryset, name, value):
        return IsActiveFilterField.is_active_filter(queryset, name, value)

    def search_qs(self, queryset, name, value):
        return SearchFilterField.search_qs(queryset, name, value,
                                           search_fields=('name', 'slug'))


class FridgeTypeForm(forms.ModelForm):
    class Meta:
        model = FridgeType
        fields = ('name', 'slug', 'create_on_user_creation')

    def clean_slug(self):
        data = super().clean()
        slug = data.get('slug')

        if not FridgeType.is_allowed_to_assign_slug(slug, instance=self.instance):
            self.add_error('slug', _(f'Fridge type with "{slug}" already exists'))

        return slug


class FridgeTypeFormAdd(FridgeTypeForm):
    pass


class FridgeTypeFormEdit(FridgeTypeForm):
    pass


class FridgeTypeImportForm(forms.Form):
    file = forms.FileField(label=_('File fixture'), required=True,
                           widget=forms.ClearableFileInput(attrs={'accept': '.json',
                                                                  'class': 'form-control file-upload-info'}))

    def clean(self):
        data = self.cleaned_data
        file = data.get('file')

        try:
            content = json.loads(file.read().decode('utf-8'))
            data['content'] = content
        except UnicodeDecodeError:
            self.add_error('file', _('File is not encoded with UTF-8'))
        except (json.JSONDecodeError, ValueError, AttributeError):
            self.add_error('file', _('File is not valid JSON'))

        return data

    def load(self):
        context = self.cleaned_data['content']

        load_fields = ('name', 'slug')
        get_by_fields = ('slug',)
        items, created_count = CrmMixinJSONLoader(model=FridgeType,
                                                  load_fields=load_fields,
                                                  get_by_fields=get_by_fields,
                                                  with_clear=False,
                                                  set_activity=False).load(context)
        return items, created_count
