from .settings import *  # noqa
from .settings import LOGGING

SECRET_KEY = 'nofollow_testing'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

KIP = {
    'DOCUMENT_STORAGE_CLASS': 'django.core.files.storage.FileSystemStorage'
}

LOGGING['handlers']['file']['filename'] = '/dev/null'
