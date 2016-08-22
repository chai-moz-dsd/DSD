from __future__ import absolute_import
import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chai.settings_prod')

logger = get_task_logger(__name__)

app = Celery('dsd', broker='redis://localhost:6379/0', backend='redis://',
             include=['dsd.service.scheduler'])

CELERY_TIMEZONE = settings.TIME_ZONE

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'tasks.add',
        'schedule': timedelta(seconds=5),
        'args': (16, 16)
    },
}

if __name__ == '__main__':
    app.start()
