from django.contrib import admin
from .models import UrlsToMonitor

# Register your models here.


class UrlsToMonitorAdmin(admin.ModelAdmin):
    list_display = ("url", "status", "last_checked")


admin.site.register(UrlsToMonitor, UrlsToMonitorAdmin)
