from django.conf.urls import url, include
from rest_framework_nested import routers

from .views import FridgeViewSet, FridgeProductViewSet, ProductViewSet

fridge_router = routers.SimpleRouter()
fridge_router.register('fridge', FridgeViewSet, basename='fridge')

fridge_products_router = routers.NestedSimpleRouter(fridge_router, r'fridge', lookup='fridge')
fridge_products_router.register(r'products', FridgeProductViewSet, basename='fridge-products')

product_router = routers.SimpleRouter()
product_router.register('product', ProductViewSet, basename='product')

url_patterns = [
    url(r'', include(fridge_router.urls)),
    url(r'', include(fridge_products_router.urls)),
    url(r'', include(product_router.urls)),
]
