from cindy.views import FeedView
from . import models


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
