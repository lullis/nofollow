from django.contrib.syndication.views import Feed as BaseFeedView
from django.utils.feedgenerator import Atom1Feed

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
        return obj.feedlink_set.select_related('link').order_by('-updated_on')

    def item_title(self, item):
        return item.title

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


class UserFeedView(FeedView):

    def get_object(self, request, userfeed_id):
        return models.UserFeed.objects.get(id=userfeed_id)

    def title(self, obj):
        return obj.feed.title

    def link(self, obj):
        return obj.feed.url

    def description(self, obj):
        return obj.feed.description

    def categories(self, obj):
        return super().categories(obj.feed)

    def items(self, obj):
        return super().items(obj.feed)

    def item_description(self, item):
        extraction = item.link.best_extraction
        return extraction and extraction.extracted_content
