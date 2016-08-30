from chai.settings import *

CRONJOBS = (
    ('* */1 * * *', 'dsd.scheduler.start'),
)

CRONTAB_DJANGO_SETTINGS_MODULE = 'chai.settings_staging'