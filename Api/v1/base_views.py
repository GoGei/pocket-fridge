from django.contrib.auth.models import AnonymousUser
from rest_framework.generics import get_object_or_404

from Api.base_views import SerializerMapBaseView
from core.Fridge.models import Fridge


class UserRelatedView(SerializerMapBaseView):
    def get_user(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            return None
        return user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.get_user()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.get_user()

        if not user:
            return queryset.none()

        queryset = queryset.filter(user=user)
        return queryset


class FridgeRelatedView(UserRelatedView):
    def get_fridge(self):
        if hasattr(self, 'current_fridge_instance'):
            return self.current_fridge_instance

        fridge_pk = self.kwargs.get('fridge_pk', None)
        if not fridge_pk:
            return None

        qs = Fridge.objects.active()
        fridge = get_object_or_404(qs, pk=fridge_pk)
        setattr(self, 'current_fridge_instance', fridge)
        return fridge

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['fridge'] = self.get_fridge()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        fridge = self.get_fridge()

        if not fridge:
            return queryset.none()

        queryset = queryset.filter(fridge=fridge)
        return queryset
