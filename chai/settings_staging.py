from chai.settings import *

CRONTAB_DJANGO_SETTINGS_MODULE = 'chai.settings_staging'

CRONJOBS = (
    ('* */1 * * *', 'dsd.scheduler.start'),
)
