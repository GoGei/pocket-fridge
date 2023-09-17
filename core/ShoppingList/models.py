"""
The above code defines two models, ShoppingList and ShoppingListProduct, for a shopping list application.
"""
from django.db import models
from core.Utils.Mixins.models import CrmMixin, UUIDPrimaryKeyMixin
from core.Fridge.models import FridgeProduct


class ShoppingList(CrmMixin, UUIDPrimaryKeyMixin):
    """
    The ShoppingList model has fields for the name of the list and the user who owns it.
    It also inherits from two mixins, CrmMixin and UUIDPrimaryKeyMixin,
    which provide additional functionality for the model.
    """
    name = models.CharField(max_length=64, db_index=True, null=True)
    user = models.ForeignKey('User.User', on_delete=models.PROTECT)

    class Meta:
        db_table = 'shopping_list'


class ShoppingListProduct(CrmMixin, UUIDPrimaryKeyMixin):
    """
    The ShoppingListProduct model represents a product that is added to a shopping list.
    """
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.PROTECT)
    product = models.ForeignKey('Fridge.FridgeProduct', on_delete=models.PROTECT, null=True)
    fridge = models.ForeignKey('Fridge.Fridge', on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=64, db_index=True)
    amount = models.IntegerField(default=1)
    units = models.CharField(max_length=16, db_index=True, choices=FridgeProduct.FridgeProductUnits.choices)

    class Meta:
        db_table = 'shopping_list_product'
