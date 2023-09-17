from rest_framework import viewsets
from .serializers import UserSerializer
from core.User.models import User


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.users()
    serializer_class = UserSerializer
