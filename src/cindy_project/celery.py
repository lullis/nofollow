from celery import Celery
from django.conf import settings


class ServiceConfig(object):
    name = settings.MESSAGE_BROKER.get('QUEUE_NAME')
    broker_url = settings.MESSAGE_BROKER.get('URL')
    broker_use_ssl = settings.MESSAGE_BROKER.get('USE_SSL', False)


app = Celery()
app.config_from_object(ServiceConfig)
app.autodiscover_tasks()
