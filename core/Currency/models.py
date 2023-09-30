"""
This code defines a Django model called "Currency" with fields such as name, code, number, and is_active.
It also includes a custom manager called "CurrencyManager" which provides methods
to retrieve the default currency and active currencies.
"""

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class CurrencyManager(models.QuerySet):
    def get_default(self):
        """
        The "get_default()" method retrieves the default currency based on the value
        of the "DEFAULT_CURRENCY" setting in the Django project's settings.
        """
        return self.get(code=settings.DEFAULT_CURRENCY_CODE)

    def active(self):
        """
        The "active()" method returns a queryset of active currencies.
        """
        return self.filter(is_active=True)


class Currency(models.Model):
    """
    The "Currency" model represents a currency with its name, code, and number.
    The "is_active" field is a boolean flag indicating whether the currency is currently active or not.
    """
    name = models.CharField(verbose_name=_('Name'), max_length=64)
    code = models.CharField(verbose_name=_('Code'), max_length=4, unique=True, blank=True)
    number = models.CharField(verbose_name=_('Number'), max_length=4, unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    objects = CurrencyManager().as_manager()

    class Meta:
        db_table = 'currency'

    def archive(self):
        self.is_active = False
        self.save()
        return self
