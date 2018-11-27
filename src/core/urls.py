from django.urls import path

from . import views

urlpatterns = [
    path('feed/<int:userfeed_id>/user', views.UserFeedView(), name='user-feed')
]
