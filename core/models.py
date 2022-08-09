from operator import mod
from statistics import mode
from urllib import request
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
status_choices = (("0", "inactive"), ("1", "active"))


class UrlsToMonitor(models.Model):
    """
    Using this model you can add url.
    If you want not to check status of url for any reason just unselect check_needed.
    Status is defined by celery task for given interval of time.
    Every time status checked last_checked will get new date
    """

    url = models.URLField(max_length=300)
    status = models.CharField(
        choices=status_choices, max_length=1, blank=True, null=True
    )
    check_needed = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_checked = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.url
