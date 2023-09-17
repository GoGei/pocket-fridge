from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from Manager.Api.base_views import AdminViewSet as BaseAdminViewSet
from core.User.models import User
from .serializers import UserSerializer



class UserViewSet(BaseAdminViewSet):
    queryset = User.objects.all().order_by('email', 'first_name', 'last_name')
    serializer_class = UserSerializer

    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering_fields = ('email', 'last_name')
    filterset_fields = ('is_active', 'is_staff', 'is_superuser')
