import logging

from celery import shared_task
from django.utils import timezone

from .models import Link, Site


logger = logging.getLogger(__name__)


@shared_task
def make_user_link(user_id, url):
    link = Link.make(url)

    user_link, _ = link.userlink_set.get_or_create(user_id=user_id, link=link)
    link.crawl()
    link.site.update_favicon()


@shared_task
def crawl_sites():
    LINKS_PER_SITE = 5
    now = timezone.now()
    logger.info('Crawling sites started at {}'.format(now))
    for site in Site.objects.iterator():
        last_crawl = site.last_crawled
        if not last_crawl or (now - last_crawl).seconds > site.crawling_frequency:
            links_to_crawl = site.link_set.filter(crawleditem__isnull=True)
            for link in links_to_crawl[:LINKS_PER_SITE]:
                link.crawl()
