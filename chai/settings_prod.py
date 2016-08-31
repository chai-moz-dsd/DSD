from chai.settings import *

CRONTAB_DJANGO_SETTINGS_MODULE = 'chai.settings_prod'

# run at 30 min
CRONJOBS = (
    ('*/30 * * * *', 'dsd.scheduler.start'),
)
