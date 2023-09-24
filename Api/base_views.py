from rest_framework import viewsets
from Api.serializers import EmptySerializer


class SerializerMapBaseView(viewsets.GenericViewSet):
    """
    Base view to implement mapping of serializers

    serializer_map - serializers to get by current action
    empty_serializer_actions - action that require empty body

    serializer_map = {
        'list': SerializerForView,
        'retrieve': SerializerForView,
        'create': SerializerForCreate,
        ...
    }
    empty_serializer_actions = {'archive', 'restore', ...}
    """

    serializer_map = dict()
    empty_serializer_actions = set()
    serializer_return_map = dict()
    serializer_return_class = None

    def get_serializer_class(self):
        if self.action in self.empty_serializer_actions:
            return EmptySerializer
        return self.serializer_map.get(self.action, self.serializer_class)

    def get_serializer_return_class(self):
        serializer_from_map = self.serializer_return_map.get(self.action)
        if serializer_from_map:
            return serializer_from_map
        return self.serializer_return_class or self.serializer_class

    def prepare_response(self, instance, many=False):
        serializer_class = self.get_serializer_return_class()
        response = serializer_class(instance=instance, many=many).data
        return response


class CrmMixinView(SerializerMapBaseView):
    def perform_create(self, serializer):
        instance = serializer.save(created_by=self.request.user)
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.modify(self.request.user)
        return instance

    def perform_destroy(self, instance):
        instance.archive(self.request.user)
        return instance
