from celery.utils.log import get_task_logger
from celery import shared_task
from .models import UrlsToMonitor
import requests
from django_celery_beat.models import PeriodicTask, IntervalSchedule

logger = get_task_logger(__name__)


@shared_task(name="check_url_task")
def check_urls():
    urls = UrlsToMonitor.objects.filter(check_needed=True)
    for item in urls:
        url = item.url
        response = requests.get(url)
        if response.status_code == 200:
            item.status = 1
        else:
            item.status = 0
        item.save()


# for the first time db populated with this info.
# However we can add new intervals from django admin
schedule, created = IntervalSchedule.objects.get_or_create(
    every=30,
    period=IntervalSchedule.SECONDS,
)

try:
    # to handle existence error
    PeriodicTask.objects.create(
        interval=schedule,  # we created this above.
        # simply describes this periodic task.
        name="Perodiaclly check status of urls in database!",
        task="check_url_task",  # name of task.
    )
except Exception as e:
    pass
