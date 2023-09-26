from rest_framework import viewsets

from Api.base_views import CrmMixinView
from Api.v1.base_views import UserRelatedView, FridgeRelatedView
from .serializers import (
    FridgeTypeSerializer, FridgeSerializer, FridgeViewSerializer, FridgeProductSerializer, FridgeProductViewSerializer
)
from core.Fridge.models import FridgeType, Fridge, FridgeProduct


class FridgeTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FridgeType.objects.active().order_by('-name')
    serializer_class = FridgeTypeSerializer


class FridgeViewSet(CrmMixinView, UserRelatedView, viewsets.ModelViewSet):
    queryset = Fridge.objects.select_related('user').active()
    serializer_class = FridgeSerializer
    serializer_map = {
        'list': FridgeViewSerializer,
        'retrieve': FridgeViewSerializer,
    }


class FridgeProductViewSet(CrmMixinView, FridgeRelatedView, viewsets.ModelViewSet):
    queryset = FridgeProduct.objects.select_related('fridge', 'user').active()
    serializer_class = FridgeProductSerializer
    serializer_return_class = FridgeProductViewSerializer
    serializer_map = {
        'list': FridgeProductViewSerializer,
        'retrieve': FridgeProductViewSerializer,
    }
