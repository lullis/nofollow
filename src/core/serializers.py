from rest_framework import serializers

from . import tasks
from . import models


class URLSubmissionSerializer(serializers.Serializer):
    url = serializers.URLField(write_only=True)


class EntrySubmissionSerializer(URLSubmissionSerializer):

    def validate(self, data):
        user = self.context['request'].user
        if user.entry_set.filter(link__url=data['url']).exists():
            raise serializers.ValidationError('URL has already submitted this link')

        return data

    def create(self, validated_data):
        link, created = models.Link.objects.get_or_create(
            url=validated_data['url']
        )

        if not link.is_processed:
            tasks.process_link(link.id)

        return models.Entry.objects.create(
            user=self.context['request'].user, link=link
        )


class UserFeedSubmissionSerializer(URLSubmissionSerializer):

    def validate(self, data):
        user = self.context['request'].user
        if user.userfeed_set.filter(feed__url=data['url']).exists():
            raise serializers.ValidationError('User is already subscribed to feed')

        return data

    def create(self, validated_data):
        feed, created = models.Feed.objects.get_or_create(
            url=validated_data['url']
        )

        if created: tasks.sync_feed.delay(feed.pk)

        return models.UserFeed.objects.create(
            feed=feed, user=self.context['request'].user
        )
