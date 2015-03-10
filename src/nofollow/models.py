#!/usr/bin/env python

import os
import hashlib
import logging

from django.conf import settings
from readability import readability
import requests


logger = logging.getLogger(__name__)


class Document(object):
    def __init__(self, url):
        self.url = url
        self._md5 = hashlib.md5(self.url).hexdigest()

    def process(self):
        response = requests.get(self.url)
        response.raise_for_status()

        readable_doc = readability.Document(response.text).summary()

        try:
            os.makedirs(os.path.dirname(self.path))
        except OSError:
            pass

        try:
            with open(self.path, 'w') as converted_file:
                converted_file.write(readable_doc.encode('utf-8'))

        except Exception, e:
            os.remove(self.path)
            logger.warn(e)
            raise e

    @property
    def hexdigest(self):
        return self._md5

    @property
    def path(self):
        return os.path.join(settings.MEDIA_ROOT, self.hexdigest, 'document.html')

    @property
    def is_processed(self):
        return os.path.exists(self.path)


class ConvertedDocument(Document):
    def __init__(self, digest):
        self._md5 = digest

    def process(self):
        return
