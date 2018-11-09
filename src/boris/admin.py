from django.contrib import admin

from . import models


@admin.register(models.CrawledItem)
class CrawledItemAdmin(admin.ModelAdmin):
    list_filter = ('spider_name', )
