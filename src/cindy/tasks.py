import logging
import datetime

from celery import shared_task
from django.utils import timezone

from . import models


logger = logging.getLogger(__name__)
HOUR_DELTA = datetime.timedelta(minutes=60)


@shared_task
def make_user_feed(user_id, url):
    feed = models.Feed.register(url)
    feed.fetch()
    return models.UserFeed.objects.create(feed=feed, user_id=user_id)


@shared_task
def fetch_feed(feed_id):
    feed = models.Feed.objects.get(id=feed_id)
    feed.fetch()


@shared_task
def register_feed(feed_url):
    models.Feed.register(feed_url)


@shared_task
def sync_feeds(timedelta=HOUR_DELTA):
    now = timezone.now()
    then = now - timedelta

    pending_feeds = models.Feed.objects.filter(
        is_active=True, last_checked__lt=then
    )

    for feed in pending_feeds.iterator():
        feed.fetch()
