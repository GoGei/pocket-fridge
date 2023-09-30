from django import forms
from django.utils.translation import gettext_lazy as _
from core.User.models import User
from core.Utils.fields import PasswordField


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True,
                             max_length=255,
                             label=_('Email'),
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control',
                                        'autofocus': 'autofocus',
                                        'placeholder': _('Enter your email')})
                             )
    first_name = forms.CharField(required=True,
                                 max_length=50,
                                 label=_('First name'),
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control',
                                            'placeholder': _('Enter your first name')})
                                 )
    last_name = forms.CharField(required=True,
                                max_length=50,
                                label=_('Last name'),
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control',
                                           'placeholder': _('Enter your last name')})
                                )
    password = PasswordField(required=True,
                             label=_('Password'),
                             widget=forms.PasswordInput(
                                 attrs={'class': 'form-control',
                                        'placeholder': _('Password')})
                             )
    confirm_password = PasswordField(required=True,
                                     label=_('Confirm password'),
                                     widget=forms.PasswordInput(
                                         attrs={'class': 'form-control',
                                                'placeholder': _('Confirm password')})
                                     )
    agree_checkbox = forms.BooleanField(required=True,
                                        widget=forms.CheckboxInput(
                                            attrs={'class': 'form-check-input'}
                                        ))

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password',
            'confirm_password',
            'agree_checkbox',
        )

    def clean(self):
        data = super().clean()

        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            msg = _('Passwords do not match')
            self.add_error('password', msg)
            self.add_error('confirm_password', msg)

        return data

    def save(self, commit=True):
        user = super().save(commit=False)

        user.is_active = False
        user.is_staff = False
        user.is_superuser = False
        user.external_id = None

        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(label=_('Email address'),
                             widget=forms.TextInput({'autofocus': 'autofocus',
                                                     'class': 'form-control',
                                                     'placeholder': _('Email address')}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput({'class': 'form-control',
                                                           'placeholder': _('Password')}))
    remember_me = forms.BooleanField(required=False,
                                     label=_('Remember me'),
                                     widget=forms.CheckboxInput(
                                         attrs={'class': 'form-check-input'}
                                     ))

    def clean_email(self):
        data = self.cleaned_data
        email = data.get('email', '')
        return email.lower()


class UserForgotPasswordForm(forms.Form):
    email = forms.EmailField(label=_('Email address'),
                             widget=forms.TextInput({'autofocus': 'autofocus',
                                                     'class': 'form-control',
                                                     'placeholder': _('Email address')}))

    def clean(self):
        data = self.cleaned_data
        email = data.get('email', '')
        email = email.lower()

        try:
            user = User.objects.active().get(email__iexact=email)
            data.update({'user': user})
        except User.DoesNotExist:
            self.add_error('email', _('User with this email not found'))
        return data


class UserResetPasswordForm(forms.Form):
    password = PasswordField(required=True,
                             label=_('Password'),
                             widget=forms.PasswordInput(
                                 attrs={'class': 'form-control',
                                        'placeholder': _('Password')})
                             )
    confirm_password = PasswordField(required=True,
                                     label=_('Confirm password'),
                                     widget=forms.PasswordInput(
                                         attrs={'class': 'form-control',
                                                'placeholder': _('Confirm password')})
                                     )

    class Meta:
        model = User
        fields = (
            'password',
            'confirm_password',
        )

    def clean(self):
        data = super().clean()

        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            msg = _('Passwords do not match')
            self.add_error('password', msg)
            self.add_error('confirm_password', msg)

        return data
