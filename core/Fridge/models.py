from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from core.Utils.Mixins.models import CrmMixin, UUIDPrimaryKeyMixin, SlugifyMixin


class FridgeType(CrmMixin, SlugifyMixin):
    SLUGIFY_FIELD = 'name'
    name = models.CharField(max_length=64, db_index=True)

    class Meta:
        db_table = 'fridge_type'


class Fridge(CrmMixin, UUIDPrimaryKeyMixin):
    name = models.CharField(max_length=64)
    user = models.ForeignKey('User.User', on_delete=models.PROTECT)
    fridge_type = models.ForeignKey(FridgeType, on_delete=models.PROTECT)

    class Meta:
        db_table = 'fridge'


class FridgeProduct(CrmMixin, UUIDPrimaryKeyMixin):
    class FridgeProductUnits(models.TextChoices):
        GRAMM = 'gramm', _('Gr')
        KILOGRAM = 'kilogram', _('KG')
        MILLITER = 'milliter', _('ML')
        LITER = 'liter', _('L')
        ITEMS = 'items', _('Items')

    name = models.CharField(max_length=64, db_index=True)
    storage = models.ForeignKey(Fridge, on_delete=models.PROTECT)
    amount = models.DecimalField(default=1, max_digits=8, decimal_places=2)
    units = models.CharField(max_length=16, db_index=True, choices=FridgeProductUnits.choices)
    manufacture_date = models.DateField(db_index=True)
    shelf_life_date = models.DateField(db_index=True)
    notes = models.CharField(max_length=2048, null=True)
    image = models.ImageField(null=True, upload_to=settings.FRIDGE_PRODUCTS_FILEPATH)
    barcode = models.CharField(max_length=64, null=True, db_index=True)

    class Meta:
        db_table = 'fridge_product'
