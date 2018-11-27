from django.contrib import admin

from . import models


@admin.register(models.UserFeed)
class UserFeedAdmin(admin.ModelAdmin):
    pass


@admin.register(models.UserLink)
class UserLinkAdmin(admin.ModelAdmin):
    pass
