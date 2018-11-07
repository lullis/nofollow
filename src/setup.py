#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='cindy',
    url='https://bitbucket.org/lullis/cindy',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
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
        'django-material',
        'django-taggit',
        'feedparser',
        'libsass',
        'pillow',
        'psycopg2-binary',
        'readability-lxml',
        'requests',
        'uwsgi'
    ],
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    keywords='crawling bookmark-manager readability feed-reader'
)
