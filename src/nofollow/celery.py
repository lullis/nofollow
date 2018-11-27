from celery import Celery
from celery.schedules import crontab

from django.conf import settings


class ServiceConfig(object):
    name = 'nofollow'
    broker_url = settings.MESSAGE_BROKER.get('URL')
    broker_use_ssl = settings.MESSAGE_BROKER.get('USE_SSL', False)
    beat_schedule = {
        'update-sites': {
            'task': 'boris.tasks.crawl_sites',
            'schedule': crontab(minute='*/1')
        },
        'update-feeds': {
            'task': 'cindy.tasks.sync_feeds',
            'schedule': crontab(minute='*/15')
        },
        'update-ipfs': {
            'task': 'kip.tasks.save_items_to_ipfs',
            'schedule': crontab(minute='*/1')
        },
    }


app = Celery()
app.config_from_object(ServiceConfig)
app.autodiscover_tasks()
