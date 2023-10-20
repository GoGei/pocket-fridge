import json
from django import forms
from django.utils import timezone
from django.utils.translation import ugettext as _

from core.Finances.stripe import exceptions
from core.Finances.stripe.handlers import CustomerHandler, SubscriptionHandler
from core.Finances.models import Price, Subscription
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


class ProfileSubscribeForm(forms.Form):
    number = forms.CharField(min_length=14, max_length=16)
    exp_month = forms.IntegerField(min_value=1, max_value=12)
    exp_year = forms.IntegerField()
    cvc = forms.CharField(min_length=3, max_length=4)
    card_name_holder = forms.CharField(max_length=150)
    price = forms.ModelChoiceField(queryset=Price.objects.active().integrated())

    def clean_number(self, value):
        if not value.isdigit():
            self.add_error('number', _('Only digits allowed'))
        return value

    def clean_cvc(self, value):
        if not value.isdigit():
            self.add_error('cvc', (_('Only digits allowed')))
        return value

    def clean_exp_year(self, value):
        if not (0 < value < 99 or 2000 < value < 2099):
            self.add_error('exp_year', (_("Two- or four-digit number representing the card's expiration year.")))
        return value

    @classmethod
    def form_expire_date_to_model(cls, data):
        exp_month = data['exp_month']
        exp_year = data['exp_year']
        if exp_year < 2000:
            exp_year += 2000

        expire_date = timezone.datetime(
            year=exp_year,
            month=exp_month,
            day=1
        ).date()
        return expire_date

    def clean(self):
        data = super().clean()
        this_month_start_date = timezone.now().date().replace(day=1)
        expire_date = self.form_expire_date_to_model(data)
        if this_month_start_date > expire_date:
            msg = _('Expire date can not be in past')
            self.add_error('number', ({'exp_year': msg}))

        return data

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def subscribe(self):
        user = self.user
        subscription = user.get_subscription()
        if subscription:
            msg = _('This user already has active subscription!')
            raise ValueError(msg)

        data = self.cleaned_data

        try:
            CustomerHandler().get_or_create(user)
        except exceptions.StripeException as e:
            raise exceptions.StripeGetOrCreateException(e)

        price = data['price']
        product = price.product
        start_date = timezone.now().date()

        subscription = Subscription(
            user=user,
            customer_internal_id=user.internal_id,
            product=product,
            price=price,
            start_date=start_date,
            end_date=None,
            currency=price.currency,
            quantity=1,
            created_by=user
        )
        subscription.save()
        subscription_handler = SubscriptionHandler()

        try:
            stripe_data = subscription_handler.create(subscription, charge_immediately=True)
        except exceptions.StripeException as e:
            raise exceptions.StripeObjectCreateException(e)

        try:
            subscription = subscription_handler.update_instance(data=stripe_data, instance=subscription)
        except exceptions.StripeException as e:
            raise exceptions.StripeObjectUpdateException(e)

        return subscription
