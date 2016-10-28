import json
import logging

import requests
from django.core.cache import cache

from chai import settings
from dsd.config import dhis2_config
from dsd.exceptions.remote_request_exception import RemoteRequestException

logger = logging.getLogger(__name__)

# TODO - Put these in ini config
HEADER_OAUTH = dhis2_config.HEADER_OAUTH
USERNAME = dhis2_config.USERNAME
PASSWORD = dhis2_config.PASSWORD
OAUTH2_UID = dhis2_config.OAUTH2_UID
OAUTH2_SECRET = dhis2_config.OAUTH2_SECRET
ACCESS_TOKEN = dhis2_config.ACCESS_TOKEN
REFRESH_TOKEN = dhis2_config.REFRESH_TOKEN
EXPIRES_TIME = dhis2_config.EXPIRES_TIME


def get_access_token():
    if cache.get(ACCESS_TOKEN):
        return cache.get(ACCESS_TOKEN)

    if not cache.get(REFRESH_TOKEN):
        set_refresh_token()

    set_access_token()

    return cache.get(ACCESS_TOKEN)


def set_access_token():
    refresh_token = cache.get(REFRESH_TOKEN)
    body = {'grant_type': REFRESH_TOKEN, REFRESH_TOKEN: refresh_token}
    response = __post_request(dhis2_config.DHIS2_STATIC_URLS.get(dhis2_config.OAUTH2_TOKEN), body,
                              (OAUTH2_UID, OAUTH2_SECRET), HEADER_OAUTH)
    json_data = json.loads(response.text)
    cache.set(ACCESS_TOKEN, json_data[ACCESS_TOKEN], EXPIRES_TIME)


def set_refresh_token():
    body = {'grant_type': 'password', 'username': USERNAME, 'password': PASSWORD}
    logger.critical(body)
    response = __post_request(dhis2_config.DHIS2_STATIC_URLS.get(dhis2_config.OAUTH2_TOKEN), body,
                              (OAUTH2_UID, OAUTH2_SECRET), HEADER_OAUTH)
    logger.critical(OAUTH2_UID)
    json_data = json.loads(response.text)
    logger.critical(json_data)
    cache.set(REFRESH_TOKEN, json_data[REFRESH_TOKEN], EXPIRES_TIME)


def create_oauth():
    body = {
        'name': 'DSD Client',
        'cid': OAUTH2_UID,
        'secret': OAUTH2_SECRET,
        'grantTypes': ['password', 'refresh_token', 'authorization_code']
    }
    HEADER_OAUTH_CREATE = {'Content-Type': 'application/json'}
    response = __post_request(dhis2_config.DHIS2_STATIC_URLS.get(dhis2_config.OAUTH2_CREATE), json.dumps(body),
                              (USERNAME, PASSWORD), HEADER_OAUTH_CREATE)
    if response.status_code == 200:
        logger.info('Create oauth successfully')
        return response
    else:
        create_oauth()


def initial_access_token():
    create_oauth()
    set_refresh_token()
    set_access_token()


def __post_request(url, data, auth, header):
    try:
        response = requests.post(url=url,
                                 data=data,
                                 auth=auth,
                                 headers=header,
                                 verify=settings.DHIS2_SSL_VERIFY)
        return response
    except ConnectionError:
        raise RemoteRequestException()
