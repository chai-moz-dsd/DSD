from chai.settings import *

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
        'NAME': 'chai',
        'USER': 'chai',
        'PASSWORD': os.getenv('CHAI_DB_PASSWORD', 'invalid_password'),
        'HOST': '52.42.224.43',
        'PORT': '5432',
        'OPTIONS': {
            'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
        },
    }
}
