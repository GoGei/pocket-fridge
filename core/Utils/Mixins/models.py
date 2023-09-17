import uuid

from django.db import models
from django.utils import timezone, translation
from django.utils.text import slugify
from django.conf import settings


class ActiveQuerySet(models.QuerySet):
    def active(self):
        return self.filter(archived_stamp__isnull=True)

    def archived(self):
        return self.filter(archived_stamp__isnull=False)

    def archive(self, archived_by=None):
        for item in self:
            item.archive(archived_by)

    def restore(self, restored_by=None):
        for item in self:
            item.restore(restored_by)

    def ordered(self):
        return self.all().order_by('-created_stamp')

    def is_active_annotated(self):
        return self.annotate(
            is_active_annotated=models.Case(
                models.When(archived_stamp__isnull=True, then=models.Value(True)),
                models.When(archived_stamp__isnull=False, then=models.Value(False)),
                default=models.Value(None),
                output_field=models.NullBooleanField
            ),
        )


class CrmMixin(models.Model):
    created_stamp = models.DateTimeField(default=timezone.now, db_index=True)
    modified_stamp = models.DateTimeField(auto_now=timezone.now)
    archived_stamp = models.DateTimeField(null=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT, related_name='+')
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT, related_name='+')
    archived_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT, related_name='+')

    objects = ActiveQuerySet.as_manager()

    class Meta:
        abstract = True

    def archive(self, archived_by=None, commit=True):
        self.archived_stamp = timezone.now()
        if archived_by:
            self.archived_by = archived_by

        if commit:
            self.save()
        return self

    def modify(self, modified_by=None, commit=True):
        self.modified_stamp = timezone.now()
        if modified_by:
            self.modified_by = modified_by

        if commit:
            self.save()
        return self

    def restore(self, restored_by=None, commit=True):
        self.archived_stamp = None
        self.archived_by = None
        self.modify(restored_by, commit=commit)
        return self

    def is_active(self) -> bool:
        return not bool(self.archived_stamp)


class SlugifyMixin(models.Model):
    SLUGIFY_FIELD = ''
    slug = models.SlugField(max_length=255, unique=True, null=True, db_index=True)

    class Meta:
        abstract = True

    @classmethod
    def value_to_slug(cls, value):
        return slugify(value)

    @classmethod
    def is_allowed_to_assign_slug(cls, value, instance=None):
        slug = cls.value_to_slug(value)
        qs = cls.objects.filter(slug=slug)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        return not qs.exists()

    @classmethod
    def generate_slug(cls, obj):
        return cls.assign_slug(obj, commit=False)

    def assign_slug(self, commit=True):
        field = self.SLUGIFY_FIELD
        if not field:
            raise ValueError('SlugifyMixin must have a slug field')

        value = getattr(self, field, None)
        if not value:
            raise ValueError('Instance must have a slug field')

        if not self.is_allowed_to_assign_slug(value, self):
            raise ValueError('It is not allowed to assign slug')

        slug = self.value_to_slug(value)
        self.slug = slug if len(slug) <= 255 else slug[:255]
        if commit:
            self.save()
        return self


class TranslateMixin(models.Model):
    TRANSLATED_FIELDS = []

    class Meta:
        abstract = True

    def __getattr__(self, key):
        if key and key in self.TRANSLATED_FIELDS:
            return getattr(self, f'{key}_data', {}).get(translation.get_language(), None)
        return super(TranslateMixin, self).__getattribute__(key)

    def __setattr__(self, key, value):
        if key and key in self.TRANSLATED_FIELDS:
            return getattr(self, f'{key}_data', {}).update({translation.get_language(): value})
        return super(TranslateMixin, self).__setattr__(key, value)

    def get_form_initial(self):
        languages = list(zip(*settings.LANGUAGES))[0]
        rc = []
        for language in languages:
            field_data = {'language_code': language}
            for field in self.TRANSLATED_FIELDS:
                data = getattr(self, '%s_data' % field).get(language, None)
                field_data.update({field: data})
            rc.append(field_data)
        return rc


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
