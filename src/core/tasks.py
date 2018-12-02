import logging

from celery import shared_task

from boris.models import Link
from boris.spiders import Spider
from cindy.models import Feed

from .models import UserFeed


logger = logging.getLogger(__name__)


@shared_task
def make_user_link(user_id, url):
    link = Link.make(url)

    user_link, _ = link.userlink_set.get_or_create(user_id=user_id, link=link)
    link.crawl()
    link.site.update_favicon()


@shared_task
def make_user_feed(user_id, url):
    feed = Feed.register(url)
    feed.fetch()
    return UserFeed.objects.create(feed=feed, user_id=user_id)


@shared_task
def handle_url_submission(user_id, url):
    try:
        response = Spider.fetch(url)
        content_type = Spider.get_content_type(response)
        action = {
            'text/html': make_user_link,
            'text/xhtml': make_user_link,
            'text/xml': make_user_link,
            'application/rss+xml': make_user_feed,
            'application/atom+xml': make_user_feed,
            'application/xml': make_user_feed
            }.get(content_type)

        return action and action(user_id, url)
    except Exception as exc:
        logger.exception(str(exc))
