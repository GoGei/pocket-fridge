from core.Utils.Mixins.models import CrmMixin
from .constants import FIELDS, DATA


class ModelJSONExporter(object):
    def __init__(self, model=None, export_fields: FIELDS = ()) -> None:
        self.model = model
        self.export_fields = export_fields

    def get_export_qs(self, queryset=None):
        if queryset:
            return queryset

        if self.model is None:
            raise ValueError('Model is not defined')

        return self.model.objects.all()

    def obj_to_dict(self, item, fields: FIELDS = None):
        data = {}
        fields = fields or self.export_fields

        if not fields:
            raise ValueError('Fields are not defined')

        for field in fields:
            data[field] = getattr(item, field)
        return data

    def export(self, queryset=None, fields: FIELDS = None) -> DATA:
        qs = self.get_export_qs(queryset=queryset)
        data = [self.obj_to_dict(item=item, fields=fields) for item in qs]
        return data


class CrmMixinJSONExporter(ModelJSONExporter):
    model: CrmMixin

    def get_export_qs(self, queryset=None):
        if queryset:
            return queryset

        qs = super().get_export_qs()
        return qs.active()
