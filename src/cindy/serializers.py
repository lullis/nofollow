from rest_framework import serializers

from . import tasks


class URLSubmissionSerializer(serializers.Serializer):
    url = serializers.URLField(write_only=True)

    def _has_submitted(self, url):
        user = self.context['request'].user
        return any([
            user.entry_set.filter(link__url=url).exists(),
            user.userfeed_set.filter(feed__url=url).exists()
            ])

    def validate(self, data):
        if self._has_submitted(data['url']):
            raise serializers.ValidationError('URL has already submitted this URL')
        return data

    def create(self, validated_data):
        return tasks.handle_url_submission(
            self.context['request'].user.id, validated_data['url']
        )


class EntrySubmissionSerializer(URLSubmissionSerializer):

    def _has_submitted(self, url):
        return self.context['request'].user.entry_set.filter(
            link__url=url
        ).exists()


class UserFeedSubmissionSerializer(URLSubmissionSerializer):

    def _has_submitted(self, url):
        return self.context['request'].user.userfeed_set.filter(feed__url=url).exists()
