from django import forms
from django.utils.translation import ugettext_lazy as _


class StripeSyncForm(forms.Form):
    external_id = forms.CharField(label=_('External ID'), max_length=32)

    def __init__(self, *args, **kwargs):
        self.handler = kwargs.pop('handler')
        super(StripeSyncForm, self).__init__(*args, **kwargs)

    def sync(self):
        external_id = self.cleaned_data.get('external_id')
        instance = self.handler().sync_from_stripe(external_id=external_id)
        return instance
