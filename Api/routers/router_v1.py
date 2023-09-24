from rest_framework import routers

from Api.v1.User.views import UserViewSet
from Api.v1.Registration.views import UserRegistrationAPIView

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='users'),
router_v1.register('register', UserRegistrationAPIView, basename='register'),
urlpatterns = router_v1.urls

urlpatterns += [
]
