from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import CurrencySerializer
from core.Currency.models import Currency


class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Currency.objects.active()
    serializer_class = CurrencySerializer
    permission_classes = (AllowAny,)
