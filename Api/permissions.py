from rest_framework.permissions import BasePermission, SAFE_METHODS
from core.Utils.Access.user_check_functions import manager_check, superuser_check


class IsStaffOrReadOnlyPermission(BasePermission):
    """
    The request is authenticated as a user and is_staff or is_superuser is True, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or manager_check(request.user))


class IsStaffPermission(BasePermission):
    """
    The request is authenticated as a user and is_staff or is_superuser is True.
    """

    def has_permission(self, request, view):
        return manager_check(request.user)


class IsAdminOrReadOnlyPermission(BasePermission):
    """
    The request is authenticated as a user and is_staff and is_superuser are True, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or superuser_check(request.user))


class IsAdminPermission(BasePermission):
    """
    The request is authenticated as a user and is_staff and is_superuser are True.
    """

    def has_permission(self, request, view):
        return superuser_check(request.user)


class IsOwnerOrReadOnlyPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or request.user and request.user.is_authenticated and obj.author.id == request.user.id)  # noqa


class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_authenticated and obj.author.id == request.user.id)  # noqa
