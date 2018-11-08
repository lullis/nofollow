import logging
import datetime

from celery import shared_task
from django.utils import timezone

from . import models


logger = logging.getLogger(__name__)
HOUR_DELTA = datetime.timedelta(minutes=60)


def make_user_entry(user_id, url):
    link, created = models.Link.objects.get_or_create(url=url)

    if not link.is_processed:
        process_link(link.id)

    return models.Entry.objects.create(
        user_id=user_id, link=link
    )


def make_user_feed(user_id, url):
    feed = models.Feed.register(url)
    feed.fetch()
    return models.UserFeed.objects.create(feed=feed, user_id=user_id)


@shared_task
def handle_url_submission(user_id, url):
    response = models.Link.fetch(url)
    response.raise_for_status()
    content_type = response.headers.get('Content-Type', '').split(';')[0]
    action = {
        'text/html': make_user_entry,
        'text/xhtml': make_user_entry,
        'application/rss+xml': make_user_feed,
        'application/atom+xml': make_user_feed
        }.get(content_type)

    return action and action(user_id, url)


@shared_task
def fetch_feed(feed_id):
    feed = models.Feed.objects.get(id=feed_id)
    feed.fetch()


@shared_task
def register_feed(feed_url):
    models.Feed.register(feed_url)


@shared_task
def process_link(link_id):
    try:
        link = models.Link.objects.get(id=link_id)
        if not link.is_processed:
            link.process()
    except Exception as exc:
        logger.exception(exc)


@shared_task
def sync_feeds(timedelta=HOUR_DELTA):
    now = timezone.now()
    then = now - timedelta

    pending_feeds = models.Feed.objects.filter(
        is_active=True, last_checked__lt=then
    )

    for feed in pending_feeds.iterator():
        feed.fetch()
