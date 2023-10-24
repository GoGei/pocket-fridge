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

    image = forms.ImageField(label=_('Photo'), required=False,
                             widget=forms.ClearableFileInput(attrs={
                                 'class': 'form-control',
                             }))

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
            'image',
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        fridge_qs = Fridge.objects.select_related('user').active().filter(user=self.user)
        self.fields['fridge'].queryset = fridge_qs
        if fridge_qs.exists():
            self.fields['fridge'].initial = fridge_qs.first().id

    def clean_notes(self):
        data = self.cleaned_data
        name = data.get('notes').strip()
        return name


class FridgeProductFormAdd(FridgeProductForm):
    def __init__(self, *args, **kwargs):
        self.fridge = kwargs.pop('fridge', None)
        super().__init__(*args, **kwargs)
        if self.fridge:
            self.fields['fridge'].initial = self.fridge.id

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance


class FridgeProductFormEdit(FridgeProductForm):
    def save(self, commit=True):
        current_image = self.cleaned_data.get('image')
        if not current_image:
            self.cleaned_data.pop('image')

        instance = super().save(commit=commit)
        return instance
