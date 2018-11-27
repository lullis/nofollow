from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel

from boris.models import Link, CrawledItem
from cindy.models import Feed

from .choices import USER_FEED_CONTENT_STYLE


class UserLink(TimeStampedModel):
    link = models.ForeignKey(Link, on_delete=models.PROTECT)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('link', 'user')


class UserFeed(TimeStampedModel):
    feed = models.ForeignKey(Feed, on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_style = models.CharField(
        max_length=16,
        choices=USER_FEED_CONTENT_STYLE,
        default=USER_FEED_CONTENT_STYLE.extracted
    )

    def get_content(self, feed_link):
        return {
            USER_FEED_CONTENT_STYLE.original: feed_link.content,
            USER_FEED_CONTENT_STYLE.summary: feed_link.summary,
            USER_FEED_CONTENT_STYLE.extracted: CrawledItem.get_extraction(feed_link.link)
        }.get(self.content_style) or ''

    def __str__(self):
        return '{} subscription from {}'.format(self.feed, self.user)

    class Meta:
        unique_together = ('feed', 'user')
