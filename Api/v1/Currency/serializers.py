from rest_framework import serializers
from core.Currency.models import Currency


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = (
            'name',
            'code',
            'number',
        )
