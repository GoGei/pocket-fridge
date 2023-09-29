"""
The above code defines four models: LicenceVersion, Licence, PrivacyPolicy, and TermsOfUse.
All models inherit from the CrmMixin class, which provides common fields and methods for CRM-related models.
"""
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from core.Utils.Mixins.models import CrmMixin, UUIDPrimaryKeyMixin, SlugifyMixin


class LicenceVersion(CrmMixin, SlugifyMixin):
    """
    The LicenceVersion model represents a version of a license.
    """
    SLUGIFY_FIELD = 'name'
    name = models.CharField(max_length=8, db_index=True)
    is_default = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = 'licence_version'

    def __str__(self):
        return str(_(f'Licence {self.name}'))

    @property
    def label(self):
        return str(self)

    def archive(self, archived_by=None, commit=True):
        instance = super().archive(archived_by=archived_by)
        Licence.objects.filter(version=instance).archive(archived_by=archived_by)
        return instance

    def set_default(self):
        LicenceVersion.objects.active().update(is_default=False)
        self.is_default = True
        self.save()
        return self

    @classmethod
    def get_default(cls):
        return cls.objects.active().filter(is_default=True).first()


class Licence(CrmMixin, UUIDPrimaryKeyMixin):
    """
    The Licence model represents a license.
    """
    name = models.CharField(max_length=128, default='Licence name')
    user = models.ForeignKey('User.User', on_delete=models.PROTECT)
    version = models.ForeignKey(LicenceVersion, on_delete=models.PROTECT)
    signed_stamp = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        db_table = 'licence'

    @classmethod
    def sign_licence_agreement(cls, user):
        version = LicenceVersion.get_default()
        if not version:
            return None
        return cls(user=user, version=version, signed_stamp=timezone.now()).save()


class PrivacyPolicy(CrmMixin, SlugifyMixin):
    """
    The PrivacyPolicy model represents a privacy policy.
    """
    SLUGIFY_FIELD = 'name'
    name = models.CharField(max_length=128, db_index=True)
    template = models.FileField(upload_to=settings.PRIVACY_POLICY_FILEPATH)
    version = models.ForeignKey(LicenceVersion, on_delete=models.PROTECT)
    is_default = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = 'privacy_policy'

    def set_default(self):
        PrivacyPolicy.objects.select_related('version').filter(version=self.version).active().update(is_default=False)
        self.is_default = True
        self.save()
        return self

    @classmethod
    def get_default(cls, version: LicenceVersion):
        return cls.objects.active().filter(version=version, is_default=True).first()


class TermsOfUse(CrmMixin, SlugifyMixin):
    """
    The TermsOfUse model represents the terms of use.
    """
    SLUGIFY_FIELD = 'name'
    name = models.CharField(max_length=128, db_index=True)
    template = models.FileField(upload_to=settings.TERMS_OF_USE_FILEPATH)
    version = models.ForeignKey(LicenceVersion, on_delete=models.PROTECT)
    is_default = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = 'terms_of_use'

    def set_default(self):
        TermsOfUse.objects.select_related('version').filter(version=self.version).active().update(is_default=False)
        self.is_default = True
        self.save()
        return self

    @classmethod
    def get_default(cls, version: LicenceVersion):
        return cls.objects.active().filter(version=version, is_default=True).first()
