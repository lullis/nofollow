from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^api/user/entries$',
        views.EntrySubmissionView.as_view(),
        name='entry-list'
    ),
    url(
        r'^api/user/feeds$',
        views.UserFeedSubmissionSerializer.as_view(),
        name='user-feed-list'
    ),
    url(
        r'^feed/(?P<feed_id>\d+)$',
        views.FeedView(),
        name='feed'
    ),
    url(
        r'^feed/(?P<feed_id>\d+)/processed$',
        views.ProcessedFeedView(),
        name='processed-feed'
    ),
    url(
        r'^entry/(?P<id>\d+)$',
        views.EntryDetailView.as_view(),
        name='entry-detail'
    )
]
