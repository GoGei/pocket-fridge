import django_filters
from django import forms
from django.utils.translation import ugettext as _
from core.Licence.models import LicenceVersion
from core.Utils.filter_fields import SearchFilterField, IsActiveFilterField


class LicenceVersionFilterForm(django_filters.FilterSet):
    search = SearchFilterField()
    is_active = IsActiveFilterField()

    def is_active_filter(self, queryset, name, value):
        return IsActiveFilterField.is_active_filter(queryset, name, value)

    def search_qs(self, queryset, name, value):
        return SearchFilterField.search_qs(queryset, name, value,
                                           search_fields=('name', 'slug'))


class LicenceVersionForm(forms.ModelForm):
    class Meta:
        model = LicenceVersion
        fields = ('name', 'slug', 'is_default')

    def clean_slug(self):
        data = super().clean()
        slug = data.get('slug')

        if not LicenceVersion.is_allowed_to_assign_slug(slug, instance=self.instance):
            self.add_error('slug', _(f'Licence version with "{slug}" already exists'))

        return slug

    def save(self, commit=True):
        instance = super().save(commit=commit)
        is_default = self.cleaned_data.get('is_default')
        if is_default:
            if commit:
                instance.set_default()
            else:
                instance.is_default = True
        return instance


class LicenceVersionFormAdd(LicenceVersionForm):
    pass


class LicenceVersionFormEdit(LicenceVersionForm):
    pass
