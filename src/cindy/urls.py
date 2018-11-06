from django.urls import path

from . import views

urlpatterns = [
    path(
        'api/user/entries',
        views.EntrySubmissionView.as_view(),
        name='entry-list'
    ),
    path(
        'api/user/feeds',
        views.UserFeedSubmissionSerializer.as_view(),
        name='user-feed-list'
    ),
    path('feed/<int:id>', views.FeedView(), name='feed'),
    path('feed/<int:id>/processed', views.ProcessedFeedView(), name='processed-feed')
]
