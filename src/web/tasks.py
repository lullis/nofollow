from celery import shared_task

from boris.spiders import Spider
from boris.tasks import make_user_link
from cindy.tasks import make_user_feed


@shared_task
def handle_url_submission(user_id, url):
    response = Spider.fetch(url)
    content_type = response.headers.get('Content-Type', '').split(';')[0]
    action = {
        'text/html': make_user_link,
        'text/xhtml': make_user_link,
        'application/rss+xml': make_user_feed,
        'application/atom+xml': make_user_feed
        }.get(content_type)

    return action and action(user_id, url)
