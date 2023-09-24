from django.conf.urls import url, include
from rest_framework_nested import routers

from .views import ShoppingListViewSet, ShoppingListProductViewSet

shopping_list_router = routers.SimpleRouter()
shopping_list_router.register('shopping-list', ShoppingListViewSet, basename='shopping-list')

shopping_list_products_router = routers.NestedSimpleRouter(shopping_list_router, r'shopping-list',
                                                           lookup='shopping_list')
shopping_list_products_router.register(r'products', ShoppingListProductViewSet, basename='shopping-list-products')

url_patterns = [
    url(r'', include(shopping_list_router.urls)),
    url(r'', include(shopping_list_products_router.urls)),
]
