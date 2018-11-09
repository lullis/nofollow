from django.urls import path

from . import views

urlpatterns = [
    path('feed/<int:feed_id>/original', views.FeedView(), name='feed'),
    path('feed/<int:userfeed_id>/user', views.UserFeedView(), name='user-feed')
]
