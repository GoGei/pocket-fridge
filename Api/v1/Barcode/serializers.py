from rest_framework import serializers


class BarcodeScannedPostSerializer(serializers.Serializer):
    image = serializers.ImageField()
