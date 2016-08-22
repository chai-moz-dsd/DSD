import logging

from celery.schedules import crontab
from celery.task import periodic_task

logger = logging.getLogger(__name__)


@periodic_task(run_every=crontab())
def pull_data():
    logger.info('periodic task...')
