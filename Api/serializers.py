from rest_framework import serializers


class EmptySerializer(serializers.Serializer):
    """
    Serializer used for actions that DO NOT required body
    """
    pass
