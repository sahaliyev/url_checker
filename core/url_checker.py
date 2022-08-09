import requests

from .models import UrlsToMonitor


def check_urls():
    urls = UrlsToMonitor.objects.filter(check_needed=True)
    for item in urls:
        url = item.url
        print(url)
