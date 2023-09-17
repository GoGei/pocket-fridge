from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class CurrencyManager(models.QuerySet):
    def get_default(self):
        return self.get(code=settings.DEFAULT_CURRENCY)

    def active(self):
        return self.filter(is_active=True)


class Currency(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=64)
    code = models.CharField(verbose_name=_('Code'), max_length=4, unique=True, blank=True)
    number = models.CharField(verbose_name=_('Number'), max_length=4, unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    objects = CurrencyManager().as_manager()

    class Meta:
        db_table = 'currency'
