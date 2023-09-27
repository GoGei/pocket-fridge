from django import forms
from django.utils.translation import ugettext as _
from core.Fridge.models import FridgeProduct


class FridgeProductForm(forms.ModelForm):
    class Meta:
        model = FridgeProduct
        fields = (
            'fridge',
            'name',
            'amount',
            'units',
            'manufacture_date',
            'shelf_life_date',
            'notes',
        )

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

    def clean_notes(self):
        data = self.cleaned_data
        name = data.get('notes').strip()
        return name


class FridgeProductFormAdd(FridgeProductForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance


class FridgeProductFormEdit(FridgeProductForm):
    class Meta(FridgeProductForm.Meta):
        model = FridgeProduct
        fields = (
            'name',
            'amount',
            'units',
            'manufacture_date',
            'shelf_life_date',
            'notes',
        )
