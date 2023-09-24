from django.db import models

from core.Fridge.models import FridgeProduct
from core.Utils.Mixins.models import CrmMixin, UUIDPrimaryKeyMixin


class ShoppingList(CrmMixin, UUIDPrimaryKeyMixin):
    name = models.CharField(max_length=64, db_index=True, null=True)
    user = models.ForeignKey('User.User', on_delete=models.PROTECT)

    class Meta:
        db_table = 'shopping_list'


class ShoppingListProduct(CrmMixin, UUIDPrimaryKeyMixin):
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.PROTECT)
    product = models.ForeignKey('Fridge.FridgeProduct', on_delete=models.PROTECT, null=True)
    fridge = models.ForeignKey('Fridge.Fridge', on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=64, db_index=True)
    amount = models.IntegerField(default=1)
    units = models.CharField(max_length=16, db_index=True, choices=FridgeProduct.FridgeProductUnits.choices)

    class Meta:
        db_table = 'shopping_list_product'
