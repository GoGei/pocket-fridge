"""
The above code defines two models, ShoppingList and ShoppingListProduct, for a shopping list application.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.Fridge.models import FridgeProduct
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

    def get_products(self):
        qs = ShoppingListProduct.objects.select_related('shopping_list', 'user', 'product', 'fridge')
        return qs.active().filter(shopping_list=self).order_by('-is_checked', 'name')

    @classmethod
    def create_shopping_list_for_user(cls, user):
        if cls.objects.select_related('user').active().filter(user=user).exists():
            raise ValueError(_(f'Shopping list for user {user.email} already exists'))
        return ShoppingList.objects.create(name='Shopping list', user=user)

    @classmethod
    def get_shopping_list(cls, user):
        qs = cls.objects.select_related('user').active().filter(user=user)
        return qs.order_by('-created_stamp').first()


class ShoppingListProduct(CrmMixin, UUIDPrimaryKeyMixin):
    """
    The ShoppingListProduct model represents a product that is added to a shopping list.
    """
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.PROTECT)
    user = models.ForeignKey('User.User', on_delete=models.PROTECT)
    product = models.ForeignKey('Fridge.FridgeProduct', on_delete=models.PROTECT, null=True)
    fridge = models.ForeignKey('Fridge.Fridge', on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=64, db_index=True)
    amount = models.DecimalField(default=1, max_digits=8, decimal_places=2)
    units = models.CharField(max_length=16, db_index=True, choices=FridgeProduct.FridgeProductUnits.choices)
    is_checked = models.BooleanField(default=True)

    class Meta:
        db_table = 'shopping_list_product'

    def __str__(self):
        return self.name

    @property
    def label(self):
        return str(self)

    def check_product(self):
        self.is_checked = True
        self.save()
        return self

    def uncheck_product(self):
        self.is_checked = False
        self.save()
        return self
