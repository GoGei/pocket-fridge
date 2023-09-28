from django import forms
from django.utils.translation import ugettext as _
from django_hosts import reverse

from core.Fridge.models import FridgeProduct, Fridge
from core.ShoppingList.models import ShoppingListProduct, ShoppingList


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


class FridgeProductForm(forms.ModelForm, BaseProductValidationForm):
    fridge = forms.ModelChoiceField(
        queryset=Fridge.objects.select_related('user').active(),
        widget=forms.Select(
            attrs={'class': 'form-control select2',
                   'placeholder': _('Select a fridge'),
                   'data-ajax-url': reverse('api-v1:fridge-list', host='api')}
        ))
    notes = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': _('Notes'), 'rows': 3, 'cols': 50}))

    manufacture_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    shelf_life_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

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


class ShoppingListProductForm(forms.ModelForm, BaseProductValidationForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.shopping_list = ShoppingList.get_shopping_list(self.user)
        super().__init__(*args, **kwargs)

    class Meta:
        model = ShoppingListProduct
        fields = (
            'name',
            'amount',
            'units',
        )

    def save(self, commit=True):
        instance = super().save(commit=False)

        instance.user = self.user
        instance.shopping_list = self.shopping_list

        product = self.cleaned_data.get('product')
        if product:
            instance.product = product
            instance.fridge = product.fridge

        if commit:
            instance.save()
        return instance


class ShoppingListProductFormAdd(ShoppingListProductForm):
    product = forms.ModelChoiceField(
        required=False,
        queryset=FridgeProduct.objects.select_related('user').active(),
        widget=forms.Select(
            attrs={'class': 'form-control select2',
                   'placeholder': _('Select a product'),
                   'data-ajax-url': reverse('api-v1:product-list', host='api')}
        ))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        qs = FridgeProduct.objects.select_related('user', 'fridge')
        self.fields['product'].queryset = qs.active().filter(user=self.user)

    class Meta(ShoppingListProductForm.Meta):
        fields = ShoppingListProductForm.Meta.fields + ('product',)


class ShoppingListProductFormEdit(ShoppingListProductForm):
    pass
