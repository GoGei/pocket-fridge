from rest_framework import viewsets
from Api.permissions import IsAdminPermission
from .serializers import UserSerializer
from core.User.models import User


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.users().filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = (IsAdminPermission,)
