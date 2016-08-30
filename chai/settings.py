"""
Django settings for chai project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
import datetime
import logging
import logging.config

import os
from os.path import join, exists

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

import psycopg2

import configparser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, 'volume/config/settings.ini'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o!0%+^r9_&u+_m9k86tb+m#dqc=@vip82a%+m+8hw=no&u*s79'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'dsd',
    'django_crontab',
    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'chai.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'dsd')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'chai.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config['LOCAL_DB']['LOCAL_DB_NAME'],
        'USER': config['LOCAL_DB']['LOCAL_DB_USERNAME'],
        'HOST': config['LOCAL_DB']['LOCAL_DB_HOST'],
        'PORT': config['LOCAL_DB']['LOCAL_DB_PORT'],
        'OPTIONS': {
            'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
        },
    },
    'chai': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config['REMOTE_DB']['REMOTE_DB_NAME'],
        'USER': config['REMOTE_DB']['REMOTE_DB_USERNAME'],
        'PASSWORD': config['REMOTE_DB']['REMOTE_DB_PASSWORD'],
        'HOST': config['REMOTE_DB']['REMOTE_DB_HOST'],
        'PORT': config['REMOTE_DB']['REMOTE_DB_PORT'],
        'OPTIONS': {
            'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
        },
    }
}

DATABASE_ROUTERS = ['dsd.routers.remote_router.RemoteRouter', 'dsd.routers.local_router.LocalRouter']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'dsd_cache',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
]

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SHELL_PLUS = "ipython"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'dsd/')

# ********************Logger configuration********************
VOLUME_ROOT = join(BASE_DIR, 'volume')
os.mkdir(VOLUME_ROOT) if not exists(VOLUME_ROOT) else None

LOGGING_DIR = join(VOLUME_ROOT, 'logs')
os.mkdir(LOGGING_DIR) if not exists(LOGGING_DIR) else None

LOG_SUFFIX = datetime.datetime.today().strftime('%Y%m%d')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(filename)s : %(funcName)s():%(lineno)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'debug_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGGING_DIR + "/debug.%s.log" % LOG_SUFFIX,
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 50,
            'formatter': 'standard'
        },
        'request_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGGING_DIR + '/django_request.%s.log' % LOG_SUFFIX,
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 50,
            'formatter': 'standard'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'debug_file'],
            'level': 'DEBUG'
        },
        'django.request': {
            'handlers': ['request_file'],
            'level': 'ERROR',
            'propagate': False
        },
        'celery.task': {
            'handlers': ['console', 'debug_file'],
            'level': 'DEBUG',
            'propagate': False
        },

        'celery.work': {
            'handlers': ['console', 'debug_file'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}
LOGGING_CONFIG = None
logging.config.dictConfig(LOGGING)

CRONJOBS = (
    ('* */1 * * *', 'dsd.scheduler.start'),
)

# DHIS2 configuration
DHIS2_SSL_VERIFY = False
DHIS2_BASE_URL = 'http://52.32.36.132:8080/'

KEY_ADD_ATTRIBUTE_TO_SCHEMAS = 'add_attribute_to_schemas'
KEY_ADD_ATTRIBUTE = 'add_attribute'
KEY_ADD_ORGANIZATION_UNIT = 'add_organization_unit'
KEY_ADD_DATA_SET_ELEMENTS = 'add_data_set_elements'
OAUTH2_TOKEN = 'oauth2_token'

DHIS2_URLS = {
    KEY_ADD_ATTRIBUTE_TO_SCHEMAS: "%sapi/24/schemas/attribute" % DHIS2_BASE_URL,
    KEY_ADD_ATTRIBUTE: "%sapi/24/attributes" % DHIS2_BASE_URL,
    KEY_ADD_ORGANIZATION_UNIT: '%sapi/24/organisationUnits' % DHIS2_BASE_URL,
    KEY_ADD_DATA_SET_ELEMENTS: '%sapi/24/dataValueSets' % DHIS2_BASE_URL,
    OAUTH2_TOKEN: "%suaa/oauth/token" % DHIS2_BASE_URL
}
