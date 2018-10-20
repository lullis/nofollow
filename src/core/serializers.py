from rest_framework import serializers


class ConverterSerializer(serializers.Serializer):
    url = serializers.URLField(required=True)
