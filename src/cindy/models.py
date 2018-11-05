import logging

from django.conf import settings
from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel
from readability import Document
import requests
from taggit.managers import TaggableManager

USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'
logger = logging.getLogger(__name__)


class AbstractFeedAuthorData(models.Model):
    author_name = models.TextField(null=True, blank=True)
    author_email = models.EmailField(null=True, blank=True)
    author_link = models.URLField(null=True, blank=True)

    class Meta:
        abstract = True


class Link(models.Model):
    url = models.URLField(unique=True)
    processed_on = models.DateTimeField(null=True)
    title = models.TextField(null=True)
    original_html = models.TextField(null=True, blank=True, editable=False)
    cleaned_html = models.TextField(null=True, blank=True, editable=False)

    @property
    def is_processed(self):
        return self.processed_on is not None

    def process(self):
        response = requests.get(self.url, headers={'User-Agent': USER_AGENT})
        try:
            response.raise_for_status()
            logger.info('Fetched {}'.format(self.url))
            contents = response.text
            doc = Document(contents)

            self.original_html = contents
            self.cleaned_html = doc.summary()
            self.processed_on = timezone.now()
            self.save()
        except requests.HTTPError as exc:
            logger.exception(str(exc))


class Feed(TimeStampedModel, AbstractFeedAuthorData):
    url = models.URLField(unique=True)
    title = models.TextField(null=True, editable=False)
    subtitle = models.TextField(null=True, blank=True, editable=False)
    info = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    etag = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    last_modified = models.DateTimeField(db_index=True, null=True, blank=True)
    last_checked = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(db_index=True, default=True)
    ttl = models.IntegerField(null=True, blank=True, help_text='Time-to-live')
    copyright = models.TextField(null=True, blank=True, editable=False)
    categories = TaggableManager()

    def __str__(self):
        if not self.title:
            return self.url

        return '{} ({})'.format(self.title, self.url)


class FeedLink(TimeStampedModel, AbstractFeedAuthorData):
    link = models.ForeignKey(Link, on_delete=models.PROTECT)
    feed = models.ForeignKey(Feed, on_delete=models.PROTECT)
    published_on = models.DateTimeField(null=True, blank=True)
    updated_on = models.DateTimeField(null=True, blank=True)
    guid = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    summary = models.TextField(null=True, blank=True, editable=False)
    content = models.TextField(null=True, blank=True, editable=False)
    copyright = models.TextField(null=True, blank=True, editable=False)
    tags = TaggableManager()

    @property
    def url(self):
        return self.link.url

    class Meta:
        unique_together = ('link', 'feed')


class Entry(TimeStampedModel):
    link = models.ForeignKey(Link, on_delete=models.PROTECT)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('link', 'user')


class UserFeed(TimeStampedModel):
    feed = models.ForeignKey(Feed, on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return '{} subscription from {}'.format(self.feed, self.user)

    class Meta:
        unique_together = ('feed', 'user')
