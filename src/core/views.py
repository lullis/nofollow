from django.contrib.syndication.views import Feed as BaseFeedView
from django.views.generic import DetailView
from django.utils.feedgenerator import Atom1Feed
from rest_framework.generics import CreateAPIView

from . import serializers
from . import models


class FeedView(BaseFeedView):
    MAX_ITEMS_PER_FEED = 100

    feed_type = Atom1Feed

    def get_object(self, request, feed_id):
        return models.Feed.objects.get(id=feed_id)

    def title(self, obj):
        return obj.title

    def link(self, obj):
        return obj.url

    def feed_url(self, obj):
        return self.link(obj)

    def description(self, obj):
        return obj.description

    def categories(self, obj):
        return [c.name for c in obj.categories.all()]

    def items(self, obj):
        return obj.feedlink_set.select_related(
            'link'
            ).order_by('-updated_on')

    def item_title(self, item):
        return item.link.title

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        return item.url

    def item_guid_is_permalink(self, item):
        return item.guid == item.url

    def item_author_name(self, item):
        return item.author_name

    def item_author_link(self, item):
        return item.author_link

    def item_author_email(self, item):
        return item.author_email

    def item_pubdate(self, item):
        return item.published_on

    def item_updateddate(self, item):
        return item.updated_on

    def item_categories(self, item):
        return [t.name for t in item.tags.all()]

    def item_copyright(self, item):
        return item.copyright


class ProcessedFeedView(FeedView):

    def item_description(self, item):
        return item.link.cleaned_html


class EntrySubmissionView(CreateAPIView):
    serializer_class = serializers.EntrySubmissionSerializer


class UserFeedSubmissionSerializer(CreateAPIView):
    serializer_class = serializers.UserFeedSubmissionSerializer


class EntryDetailView(DetailView):
    model = models.Entry
