"""
The above code defines four models: LicenceVersion, Licence, PrivacyPolicy, and TermsOfUse.
All models inherit from the CrmMixin class, which provides common fields and methods for CRM-related models.
"""
from django.db import models
from django.utils import timezone
from django.conf import settings
from core.Utils.Mixins.models import CrmMixin, UUIDPrimaryKeyMixin, SlugifyMixin


class LicenceVersion(CrmMixin, SlugifyMixin):
    """
    The LicenceVersion model represents a version of a license.
    """
    SLUGIFY_FIELD = 'name'
    name = models.CharField(max_length=8, db_index=True)

    class Meta:
        db_table = 'licence_version'


class Licence(CrmMixin, UUIDPrimaryKeyMixin):
    """
    The Licence model represents a license.
    """
    name = models.CharField(max_length=128)
    user = models.ForeignKey('User.User', on_delete=models.PROTECT)
    version = models.ForeignKey(LicenceVersion, on_delete=models.PROTECT)
    signed_stamp = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        db_table = 'licence'


class PrivacyPolicy(CrmMixin, SlugifyMixin):
    """
    The PrivacyPolicy model represents a privacy policy.
    """
    SLUGIFY_FIELD = 'name'
    name = models.CharField(max_length=128, db_index=True)
    template = models.FileField(upload_to=settings.PRIVACY_POLICY_FILEPATH)
    version = models.ForeignKey(LicenceVersion, on_delete=models.PROTECT)

    class Meta:
        db_table = 'privacy_policy'


class TermsOfUse(CrmMixin, SlugifyMixin):
    """
    The TermsOfUse model represents the terms of use.
    """
    SLUGIFY_FIELD = 'name'
    name = models.CharField(max_length=128, db_index=True)
    template = models.FileField(upload_to=settings.TERMS_OF_USE_FILEPATH)
    version = models.ForeignKey(LicenceVersion, on_delete=models.PROTECT)

    class Meta:
        db_table = 'terms_of_use'
