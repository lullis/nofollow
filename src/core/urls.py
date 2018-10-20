from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^convert$', views.ConversionView.as_view()),
    url(r'^(?P<doc_hash>[0-9a-f]+)$', views.DocumentView.as_view(), name='document-detail')
]
