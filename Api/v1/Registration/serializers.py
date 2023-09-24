from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from core.User.models import User
from Api.fields import UserPasswordField


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
        )


class RegisterSerializer(serializers.ModelSerializer):
    password = UserPasswordField(write_only=True)
    confirm_password = UserPasswordField(write_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password',
            'confirm_password',
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, data):
        data = super().validate(data)

        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError(_('Passwords do not match'))

        return data

    def save(self, **kwargs):
        kwargs.update({
            'username': None,
            'photo': None,
            'is_active': False,
            'is_staff': False,
            'is_superuser': False,
            'external_id': None,
        })

        password = self.validated_data.pop('password')
        self.validated_data.pop('confirm_password')

        instance = super().save(**kwargs)

        instance.set_password(password)
        instance.save()
        return instance


class RegisterReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'is_active',
        )


class RegistrationActivateSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=64)

    def validate(self, data):
        user = User.get_by_registration_key(data.get('key'))

        if not user:
            raise serializers.ValidationError(_('For this key user not found'))

        if user.is_active is True:
            raise serializers.ValidationError(_('User is already active'))

        data.update({'user': user})
        return data

    def activate(self):
        data = self.validated_data
        user = data.get('user')
        user = user.activate()
        user.clear_registration_keys(data.get('key'))
        return user
