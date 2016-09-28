from chai.settings import *

CRONTAB_DJANGO_SETTINGS_MODULE = 'chai.settings_dev'

# run at every minute
CRONJOBS = (
    ('*/1 * * * *', 'dsd.scheduler.start'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dsd',
        'USER': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
        },
    },
    'chai': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mBES',
        'USER': 'thoughtworks_s',
        'PASSWORD': 'ybtigloccicus.76C',
        'HOST': '52.77.118.49',
        'PORT': '5432',
        'OPTIONS': {
            'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
        },
    }
}
