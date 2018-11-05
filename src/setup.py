#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='cindy',
    url='https://bitbucket.org/lullis/cindy',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'boto3',
        'celery',
        'dateparser',
        'django>=2.0',
        'django-allauth',
        'django_compressor',
        'django-model-utils',
        'djangorestframework',
        'django-rest-auth',
        'django_smtp_ssl',
        'django-storages',
        'django-material',
        'django-taggit',
        'feedparser',
        'pillow',
        'psycopg2-binary',
        'readability-lxml',
        'requests',
        'uwsgi'
    ],
    zip_safe=False,
    classifiers=[
        'Operating System :: Linux'
    ],
    keywords='crawling bookmark-manager readability feed-reader'
)
