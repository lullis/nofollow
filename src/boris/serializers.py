from rest_framework import serializers

from . import models


class LinkSerializer(serializers.ModelSerializer):
    url = serializers.URLField()

    class Meta:
        model = models.Link
        fields = ('url', )
