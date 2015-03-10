#!/usr/bin/env python

from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns(
    '',
    url(r'^convert$', views.ConversionView.as_view()),
    url(r'^(?P<doc_hash>[0-9a-f]+)$', views.DocumentView.as_view(), name='document-detail')
)
