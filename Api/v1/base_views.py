from django.contrib.auth.models import AnonymousUser
from rest_framework.generics import get_object_or_404

from Api.base_views import SerializerMapBaseView
from core.Fridge.models import Fridge
from core.ShoppingList.models import ShoppingList


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

        user = self.get_user()
        if not user:
            return None

        qs = Fridge.objects.select_related('user').active().filter(user=user)
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


class ShoppingListRelatedView(UserRelatedView):
    def get_shopping_list(self):
        if hasattr(self, 'current_shopping_list_instance'):
            return self.current_shopping_list_instance

        shopping_list_pk = self.kwargs.get('shopping_list_pk', None)
        if not shopping_list_pk:
            return None

        user = self.get_user()
        if not user:
            return None

        qs = ShoppingList.objects.select_related('user').active().filter(user=user)
        shopping_list = get_object_or_404(qs, pk=shopping_list_pk)
        setattr(self, 'current_shopping_list_instance', shopping_list)
        return shopping_list

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['shopping_list'] = self.get_shopping_list()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        shopping_list = self.get_shopping_list()

        if not shopping_list:
            return queryset.none()

        queryset = queryset.filter(shopping_list=shopping_list)
        return queryset
