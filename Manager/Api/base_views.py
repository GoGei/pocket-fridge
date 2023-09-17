from rest_framework.viewsets import ReadOnlyModelViewSet
from Api.base_views import SerializerMapBaseView
from Api.permissions import IsStaffPermission


class AdminViewSet(ReadOnlyModelViewSet, SerializerMapBaseView):
    permission_classes = (IsStaffPermission,)
