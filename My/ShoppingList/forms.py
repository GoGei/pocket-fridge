from django import forms
from django.utils.translation import ugettext as _
from django_hosts import reverse

from My.forms import BaseProductValidationForm
from core.Fridge.models import FridgeProduct
from core.ShoppingList.models import ShoppingListProduct, ShoppingList


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
                   'data-ajax-url': reverse('api-v1:product-list', host='api'),
                   'data-base-url': reverse('api-v1:product-list', host='api'),  # base URL to get detail view
                   }
        ))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        qs = FridgeProduct.objects.select_related('user', 'fridge')
        self.fields['product'].queryset = qs.active().filter(user=self.user)

    class Meta(ShoppingListProductForm.Meta):
        fields = ShoppingListProductForm.Meta.fields + ('product',)


class ShoppingListProductFormEdit(ShoppingListProductForm):
    pass
