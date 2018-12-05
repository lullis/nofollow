#!/usr/bin/env python

from setuptools import setup, find_packages
import versioneer

setup(
    name='nofollow',
    url='https://github.com/lullis/nofollow',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'celery',
        'django>=2.0',
        'django-boris',
        'django-cindy',
        'django_compressor',
        'django-kip',
        'django-model-utils',
        'djangorestframework',
        'django-material',
        'libsass',
        'psycopg2-binary'
    ],
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ],
    keywords='bookmark-manager syndication html-extraction'
)
