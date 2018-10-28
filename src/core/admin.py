from django.contrib import admin

from . import models


@admin.register(models.UserFeed)
class UserFeedAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Entry)
class EntryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Feed)
class FeedAdmin(admin.ModelAdmin):
    pass
