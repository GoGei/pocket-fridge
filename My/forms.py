from django import forms
from django.utils.translation import ugettext as _

from core.Fridge.models import FridgeProduct


class BaseProductValidationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        name_attrs = {
            'no_label': True,
            'placeholder': _('Product name'),
        }
        if self.fields.get('name'):
            self.fields['name'].widget.attrs.update(name_attrs)

        if self.fields.get('amount'):
            self.fields['amount'].label = _('Amount')

        if self.fields.get('units'):
            self.fields['units'].label = _('Units')
            self.fields['units'].initial = FridgeProduct.FridgeProductUnits.choices[0]

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
