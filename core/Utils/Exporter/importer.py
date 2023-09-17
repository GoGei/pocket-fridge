from typing import List, Tuple
from django.db import models
from .constants import FIELDS, DATA, ITEM
from .validators import check_unique


class ModelJSONLoader(object):
    def __init__(self, model, load_fields: FIELDS, get_by_fields: FIELDS, with_clear: bool = False) -> None:
        self.model = model
        self.load_fields = load_fields
        self.get_by_fields = get_by_fields
        self.with_clear = with_clear

    def clear_previous(self):
        self.model.objects.all().delete()

    @classmethod
    def validate_before_load(cls, data):
        check_unique(data=data, field='id')

    def create(self, item: ITEM, commit: bool = True):
        qs = self.model.objects.filter(**{k: v for k, v in item.items() if k in self.get_by_fields})

        if qs.count() > 1:
            raise models.Model.MultipleObjectsReturned

        obj = qs.first()
        created = False
        if not obj:
            obj = self.model(**item)
            created = True
        else:
            [setattr(obj, field, value) for field, value in item.items()]

        if commit:
            obj.save()
        return obj, created

    def load(self, data: DATA, commit: bool = True) -> Tuple[List, int]:
        if self.with_clear:
            self.clear_previous()
        self.validate_before_load(data)

        items = list()
        created_count = 0
        for item in data:
            obj, created = self.create(item=item, commit=commit)
            if created:
                created_count += 1
            items.append(obj)

        return items, created_count


class CrmMixinJSONLoader(ModelJSONLoader):
    def __init__(self, **kwargs) -> None:
        self.set_activity = kwargs.pop('set_activity', False)
        super().__init__(**kwargs)

    def clear_previous(self):
        self.model.objects.all().archive()

    def create(self, item: ITEM, commit: bool = True):
        is_active = item.pop('is_active', False)
        obj, created = super().create(item=item, commit=False)

        if self.set_activity:
            if not is_active:
                obj.archive(commit=commit)
            elif is_active and not obj.is_active():
                obj.restore(commit=commit)

        if commit:
            obj.save()
        return obj, created
