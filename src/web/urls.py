from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path(
        'login',
        LoginView.as_view(template_name='web/login.tmpl.html'),
        name='login'
        ),
    path('logout', LogoutView.as_view(), name='logout'),
    path('dashboard', views.LinkListView.as_view(), name='dashboard'),
    path('links', views.LinkListView.as_view(), name='link-list'),
    path('feeds', views.FeedListView.as_view(), name='feed-list'),
    path('submit', views.SubmissionView.as_view(), name='submission'),
    path('read/<int:id>', views.LinkView.as_view(), name='read-link')
]
