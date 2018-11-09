from urllib.parse import urlparse

from readability import Document

from .base import Spider


class ReadabilitySpider(Spider):
    CONTENT_TYPES = ['text/html', 'text/xhtml']

    @classmethod
    def can_crawl_url(cls, url, **credentials):
        # Homepages almost never work with readability
        return bool(urlparse(url).path.strip('/'))

    def crawl(self):
        response = Spider.fetch(self._url)
        doc = Document(response.text)

        return {
            'original_content': response.text,
            'extracted_content': Spider.sanitize(doc.summary()),
            'title': doc.title()
            }
