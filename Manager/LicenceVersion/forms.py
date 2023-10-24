import django_filters
from django import forms
from django.utils.translation import ugettext as _
from core.Licence.models import LicenceVersion, PrivacyPolicy, TermsOfUse
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
    terms_of_use_template = forms.FileField(
        label=_('Terms of use template'),
        required=True, allow_empty_file=True,
        widget=forms.ClearableFileInput(attrs={'accept': '.pdf', 'class': 'form-control file-upload-info'})
    )
    privacy_policy_template = forms.FileField(
        label=_('Privacy policy template'),
        required=True, allow_empty_file=True,
        widget=forms.ClearableFileInput(attrs={'accept': '.pdf', 'class': 'form-control file-upload-info'})
    )

    class Meta:
        model = LicenceVersion
        fields = ('name', 'slug', 'is_default', 'terms_of_use_template', 'privacy_policy_template')

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
    def save(self, commit=True):
        instance = super().save()
        kwargs = {
            'name': instance.name,
            'slug': instance.slug,
            'version': instance,
            'is_default': True,
        }
        privacy_policy = PrivacyPolicy(template=self.cleaned_data.get('privacy_policy_template'), **kwargs)
        terms_of_use = TermsOfUse(template=self.cleaned_data.get('terms_of_use_template'), **kwargs)

        if commit:
            privacy_policy.save()
            terms_of_use.save()
        return instance


class LicenceVersionFormEdit(LicenceVersionForm):
    def save(self, commit=True):
        instance = super().save()

        privacy_policy = PrivacyPolicy.get_default(instance)
        terms_of_use = TermsOfUse.get_default(instance)

        privacy_policy.template = self.cleaned_data.get('privacy_policy_template')
        terms_of_use.template = self.cleaned_data.get('terms_of_use_template')

        if commit:
            privacy_policy.save()
            terms_of_use.save()
        return instance
