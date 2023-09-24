from django.conf.urls import url, include
from rest_framework import routers

from Api.v1.User.views import UserViewSet
from Api.v1.Fridge.views import FridgeTypeViewSet
from Api.v1.Registration.views import UserRegistrationAPIView

from Api.v1.Fridge.routers import url_patterns as fridge_urls

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='users'),
router_v1.register('fridge-type', FridgeTypeViewSet, basename='users'),
router_v1.register('register', UserRegistrationAPIView, basename='register'),
urlpatterns = router_v1.urls

urlpatterns += [
    url(r'^', include(fridge_urls), name='fridge'),
]
