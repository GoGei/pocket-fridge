from django import forms
from django.utils.translation import ugettext as _
from django_hosts import reverse

from core.Fridge.models import FridgeProduct, Fridge
from My.forms import BaseProductValidationForm


class FridgeProductForm(forms.ModelForm, BaseProductValidationForm):
    fridge = forms.ModelChoiceField(
        label=_('Fridge'),
        queryset=Fridge.objects.select_related('user').active(),
        widget=forms.Select(
            attrs={'class': 'form-control select2',
                   'placeholder': _('Select a fridge'),
                   'data-ajax-url': reverse('api-v1:fridge-list', host='api')}
        ))
    notes = forms.CharField(
        label=_('Notes'),
        required=False,
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': _('Leave your notes'), 'rows': 3, 'cols': 50}))

    manufacture_date = forms.DateField(
        label=_('Manufacture date'),
        widget=forms.DateInput(attrs={'type': 'date'}))
    shelf_life_date = forms.DateField(
        label=_('Shelf life date'),
        widget=forms.DateInput(attrs={'type': 'date'}))

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

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['fridge'].queryset = Fridge.objects.select_related('user').active().filter(user=self.user)

        self.fields['name'].label = _('Product name')
        self.fields['amount'].label = _('Amount')
        self.fields['units'].label = _('Units')

    def clean_notes(self):
        data = self.cleaned_data
        name = data.get('notes').strip()
        return name


class FridgeProductFormAdd(FridgeProductForm):
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance


class FridgeProductFormEdit(FridgeProductForm):
    pass
    # class Meta(FridgeProductForm.Meta):
    #     model = FridgeProduct
    #     fields = (
    #         'name',
    #         'amount',
    #         'units',
    #         'manufacture_date',
    #         'shelf_life_date',
    #         'notes',
    #     )
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields.pop('fridge')
