from chai.settings import *

CRONTAB_DJANGO_SETTINGS_MODULE = 'chai.settings_prod'

# run at every hour
CRONJOBS = (
    ('0 * * * *', 'dsd.scheduler.start'),
)
