import logging
import datetime

from celery import shared_task
from dateparser import parse
from django.conf import settings
from django.utils import timezone
import feedparser

from . import models


logger = logging.getLogger(__name__)
EPOCH = datetime.datetime.fromtimestamp(0)
HOUR_DELTA = datetime.timedelta(minutes=60)


def first_of(entry, *attrs):
    for attr in attrs:
        try:
            return entry[attr]
        except KeyError:
            pass

    return None


def parsed_datetime(timestamp):
    return parse(timestamp, settings={'TO_TIMEZONE': settings.TIME_ZONE})


@shared_task
def fetch(feed_id):
    feed = models.Feed.objects.get(id=feed_id)
    result = feedparser.parse(feed.url)
    last_checked_time_tuple = (feed.last_checked or EPOCH).timetuple()
    for entry in result.entries:
        if entry.get('updated_parsed') > last_checked_time_tuple:
            link, _ = models.Link.objects.get_or_create(
                url=entry.link, defaults={
                    'title': entry.title
                })

            author_detail = entry.get('author_detail', {})
            feed_link, _ = models.FeedLink.objects.get_or_create(
                link=link, feed=feed, defaults={
                    'summary': entry.summary,
                    'content': entry.content[0].value,
                    'published_on': parsed_datetime(entry.published),
                    'updated_on': parsed_datetime(entry.updated),
                    'author_name': author_detail.get('name'),
                    'author_link': author_detail.get('link'),
                    'author_email': author_detail.get('email'),
                    'guid': first_of(entry, 'id', 'post-id'),
                    'copyright': entry.get('copyright')
                })
            if not link.is_processed:
                process_link.delay(link.id)
        else:
            logger.info('Skipping entry {}. (updated before last run)'.format(
                entry.id
            ))


@shared_task
def register_feed(feed_url):
    if not models.Feed.objects.filter(url=feed_url).exists():
        result = feedparser.parse(feed_url)
        models.Feed.objects.create(
            url=feed_url,
            title=result.feed.title,
            subtitle=result.feed.subtitle,
            language=result.feed.language,
            etag=result.etag,
            last_modified=parsed_datetime(result.updated)
        )


@shared_task
def process_link(link_id):
    try:
        link = models.Link.objects.get(id=link_id)
        if not link.is_processed:
            link.process()
    except Exception:
        logger.exception()


@shared_task
def sync_feed(feed_id):
    try:
        feed = models.Feed.objects.get(id=feed_id)
        fetch(feed)
    except Exception:
        logger.exception()


@shared_task
def sync_feeds(timedelta=HOUR_DELTA):
    now = timezone.now()
    then = now - timedelta

    pending_feeds = models.Feed.objects.filter(
        is_active=True, last_checked__lt=then
    )

    for feed in pending_feeds.iterator():
        feed.fetch()
