from typing import Optional

import django_filters
from django import forms
from django.db import models
from django.utils.translation import ugettext as _
from core.User.models import User
from core.Utils.fields import PasswordField
from core.Utils.filter_fields import SearchFilterField, IsActiveFilterField, IsFilledFilterForm


class StatusChoices(models.TextChoices):
    STAFF = ('staff', _('Staff'))
    SUPERUSER = ('superuser', _('Superuser'))


class AdminFilterForm(django_filters.FilterSet):
    search = SearchFilterField()
    is_active = IsActiveFilterField()
    is_email_filled = IsFilledFilterForm(label=_('Is email filled'),
                                         method='is_email_filled_filter')
    is_name_filled = IsFilledFilterForm(label=_('Is name filled'),
                                        method='is_name_filled_filter')
    is_phone_filled = IsFilledFilterForm(label=_('Is phone filled'),
                                         method='is_phone_filled_filter')
    admin_status = django_filters.ChoiceFilter(label=_('Admin status'), method='admin_status_filter',
                                               choices=StatusChoices.choices,
                                               empty_label=_('Please, select value')
                                               )

    def is_active_filter(self, queryset, name, value):
        return IsActiveFilterField.is_active_filter(queryset, name, value,
                                                    activity_field='is_active')

    def search_qs(self, queryset, name, value):
        return SearchFilterField.search_qs(queryset, name, value,
                                           search_fields=('first_name', 'last_name', 'email', 'phone'))

    def is_email_filled_filter(self, queryset, name, value):
        return IsFilledFilterForm.is_filled_filter(queryset, name, value,
                                                   fields='email')

    def is_name_filled_filter(self, queryset, name, value):
        return IsFilledFilterForm.is_filled_filter(queryset, name, value,
                                                   fields=('first_name', 'last_name'))

    def is_phone_filled_filter(self, queryset, name, value):
        return IsFilledFilterForm.is_filled_filter(queryset, name, value,
                                                   fields='phone')

    def admin_status_filter(self, queryset, name, value):
        if value:
            if value == 'staff':
                queryset = queryset.filter(is_staff=True)
            elif value == 'superuser':
                queryset = queryset.filter(is_superuser=True)
        return queryset


class AdminForm(forms.ModelForm):
    status = forms.ChoiceField(choices=StatusChoices.choices)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone',
                  'is_active', 'status')
        exclude = ('is_staff', 'is_superuser')

    @classmethod
    def to_status(cls, admin) -> Optional[StatusChoices]:
        if admin.is_superuser:
            return StatusChoices.SUPERUSER
        elif admin.is_staff:
            return StatusChoices.STAFF
        else:
            return None

    def clean(self):
        data = super().clean()
        status = data.get('status')

        if status == StatusChoices.STAFF:
            self.instance.is_staff = True
            self.instance.is_superuser = False
        elif status == StatusChoices.SUPERUSER:
            self.instance.is_staff = True
            self.instance.is_superuser = True
        else:
            self.add_error('status', _('Invalid status'))
        return data


class AdminFormAdd(AdminForm):
    pass


class AdminFormEdit(AdminForm):
    pass


class AdminSetPasswordForm(forms.Form):
    password = PasswordField()
    confirm_password = PasswordField()

    def __init__(self, *args, **kwargs):
        self.admin = kwargs.pop('admin')
        super().__init__(*args, **kwargs)

    def clean(self):
        data = super().clean()
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            self.add_error('password', _('Passwords do not match'))
        return data

    def save(self, commit=True):
        self.admin.set_password(self.cleaned_data['password'])
        if commit:
            self.admin.save()
        return self.admin


class AdminResetPasswordForm(forms.Form):
    current_password = PasswordField(with_uppercase=False, with_lowercase=False, with_special=False, with_digits=False)
    password = PasswordField()
    confirm_password = PasswordField()

    def __init__(self, *args, **kwargs):
        self.admin = kwargs.pop('admin')
        super().__init__(*args, **kwargs)

    def clean(self):
        data = super().clean()

        current_password = data.get('current_password')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if not self.admin.check_password(current_password):
            self.add_error('current_password', _('Current password is incorrect'))

        if password != confirm_password:
            self.add_error('password', _('Passwords do not match'))

        if current_password == password:
            self.add_error('current_password', _('Current password is the same as new password'))

        return data

    def save(self, commit=True):
        self.admin.set_password(self.cleaned_data['password'])
        if commit:
            self.admin.save()
        return self.admin
