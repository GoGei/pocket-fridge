from rest_framework import viewsets
from rest_framework.decorators import action

from Api.base_views import CrmMixinView
from Api.v1.base_views import UserRelatedView, ShoppingListRelatedView
from .serializers import (
    ShoppingListSerializer, ShoppingListProductSerializer, ShoppingListProductViewSerializer,
    ShoppingListProductCreateFromProductSerializer
)
from core.ShoppingList.models import ShoppingList, ShoppingListProduct


class ShoppingListViewSet(CrmMixinView, UserRelatedView, viewsets.ModelViewSet):
    queryset = ShoppingList.objects.select_related('user').active()
    serializer_class = ShoppingListSerializer


class ShoppingListProductViewSet(CrmMixinView, ShoppingListRelatedView, viewsets.ModelViewSet):
    queryset = ShoppingListProduct.objects.active()
    queryset = queryset.select_related('shopping_list', 'user', 'product', 'fridge', 'product__fridge')

    serializer_class = ShoppingListProductSerializer
    serializer_return_class = ShoppingListProductViewSerializer
    serializer_map = {
        'list': ShoppingListProductViewSerializer,
        'retrieve': ShoppingListProductViewSerializer,
        'create_from_product': ShoppingListProductCreateFromProductSerializer,
    }

    @action(methods=['post'], detail=False, url_path='create-from-product', url_name='create-from-product')
    def create_from_product(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
