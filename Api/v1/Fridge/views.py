from rest_framework import viewsets

# from Api.base_views import CrmMixinView
from Api.v1.base_views import UserRelatedView, FridgeRelatedView
from .serializers import (
    FridgeTypeSerializer, FridgeSerializer, FridgeViewSerializer, FridgeProductSerializer, FridgeProductViewSerializer,
    ProductSerializer, ProductViewSerializer
)
from core.Fridge.models import FridgeType, Fridge, FridgeProduct


class FridgeTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FridgeType.objects.active().order_by('-name')
    serializer_class = FridgeTypeSerializer


# class FridgeViewSet(CrmMixinView, UserRelatedView, viewsets.ModelViewSet):
class FridgeViewSet(UserRelatedView, viewsets.ReadOnlyModelViewSet):
    queryset = Fridge.objects.select_related('user').active()
    serializer_class = FridgeSerializer
    serializer_map = {
        'list': FridgeViewSerializer,
        'retrieve': FridgeViewSerializer,
    }


# class FridgeProductViewSet(CrmMixinView, FridgeRelatedView, viewsets.ModelViewSet):
class FridgeProductViewSet(FridgeRelatedView, viewsets.ReadOnlyModelViewSet):
    queryset = FridgeProduct.objects.select_related('fridge', 'user').active()
    serializer_class = FridgeProductSerializer
    serializer_return_class = FridgeProductViewSerializer
    serializer_map = {
        'list': FridgeProductViewSerializer,
        'retrieve': FridgeProductViewSerializer,
    }


class ProductViewSet(UserRelatedView, viewsets.ReadOnlyModelViewSet):
    queryset = FridgeProduct.objects.select_related('fridge', 'user').active()
    serializer_class = ProductSerializer
    serializer_return_class = ProductViewSerializer
    serializer_map = {
        'list': ProductViewSerializer,
        'retrieve': ProductViewSerializer,
    }
