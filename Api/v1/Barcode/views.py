from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from Api.base_views import SerializerMapBaseView
from .serializers import BarcodeScannedPostSerializer


class BarcodeAPIView(SerializerMapBaseView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    serializer_map = {
        'scanner': BarcodeScannedPostSerializer,
    }

    @action(detail=False, methods=['post'], url_name='scanner', url_path='scanner')
    def scanner(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.get_barcode_data()
        return Response(data, status=status.HTTP_200_OK)
