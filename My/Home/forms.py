import json
from django import forms
from django.utils.translation import ugettext as _
from core.User.services import load_user_fridge_data


class ProfileImportForm(forms.Form):
    file = forms.FileField(label=_('File fixture'), required=True,
                           widget=forms.ClearableFileInput(attrs={'accept': '.json',
                                                                  'class': 'form-control file-upload-info'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        data = self.cleaned_data
        file = data.get('file')

        try:
            content = json.loads(file.read().decode('utf-8'))
            data['content'] = content
        except UnicodeDecodeError:
            self.add_error('file', _('File is not encoded with UTF-8'))
        except (json.JSONDecodeError, ValueError, AttributeError):
            self.add_error('file', _('File is not valid JSON'))

        return data

    def load(self):
        content = self.cleaned_data['content']
        try:
            load_user_fridge_data(self.user, content)
        except Exception as e:
            raise ValueError(_('Unable to load file. Error: %s') % str(e))
