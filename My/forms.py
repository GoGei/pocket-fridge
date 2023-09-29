from django import forms
from django.utils.translation import ugettext as _


class BaseProductValidationForm(forms.Form):
    def clean_name(self):
        data = self.cleaned_data
        name = data.get('name').strip()
        return name

    def clean_amount(self):
        data = self.cleaned_data
        amount = data.get('amount')
        if amount < 0:
            self.add_error('amount', _('Amount cannot be negative'))
        return amount
