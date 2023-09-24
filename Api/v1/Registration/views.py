from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from Api.base_views import SerializerMapBaseView
from .serializers import RegisterSerializer, RegistrationActivateSerializer, RegisterReturnSerializer, UserRegisterSerializer


class UserRegistrationAPIView(SerializerMapBaseView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    serializer_class = UserRegisterSerializer
    serializer_return_class = UserRegisterSerializer

    serializer_map = {
        'register': RegisterSerializer,
        'activate': RegistrationActivateSerializer,
    }
    serializer_return_map = {
        'register': RegisterSerializer,
        'activate': RegisterReturnSerializer,
    }

    @action(detail=False, methods=['post'])
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.send_registration_email()
        response = self.prepare_response(user)
        return Response(response, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get', 'post'],
            pagination_class=None, filter_backends=None)
    def activate(self, request, *args, **kwargs):
        if request.method == 'GET':
            key = request.GET.get('key', None)
            data = {'key': key}
        else:
            data = request.data

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.activate()
        response = self.prepare_response(user)
        return Response(response, status=status.HTTP_200_OK)
