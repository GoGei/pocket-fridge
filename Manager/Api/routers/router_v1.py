from rest_framework import routers

from Manager.Api.v1.User.views import UserViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='manager-users'),
urlpatterns = router_v1.urls

urlpatterns += [
]
