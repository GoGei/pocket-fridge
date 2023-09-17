from django.db import models
from django.conf import settings
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
        GRAMM = 'gramm', 'Gr'
        KILOGRAM = 'kilogram', 'KG'
        MILLITER = 'milliter', 'ML'
        LITER = 'liter', 'L'
        ITEMS = 'items', 'Items'

    name = models.CharField(max_length=64, db_index=True)
    storage = models.ForeignKey(Fridge, on_delete=models.PROTECT)
    amount = models.IntegerField(default=1)
    units = models.CharField(max_length=16, db_index=True, choices=FridgeProductUnits.choices)
    manufacture_date = models.DateField(db_index=True)
    shelf_life_date = models.DateField(db_index=True)
    notes = models.CharField(max_length=2048, null=True)
    image = models.ImageField(null=True, upload_to=settings.FRIDGE_PRODUCTS_FILEPATH)
    barcode = models.CharField(max_length=64, null=True, db_index=True)

    class Meta:
        db_table = 'fridge_product'
