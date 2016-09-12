import json

import requests
from django.core.cache import cache

from chai import settings
from dsd.config import dhis2_config
from dsd.exceptions.remote_request_exception import RemoteRequestException

# TODO - Put these in ini config
HEADER_OAUTH = {'Accept': 'application/json'}
USERNAME = 'admin'
PASSWORD = 'district'
OAUTH2_UID = 'moh'
OAUTH2_SECRET = '1e6db50c-0fee-11e5-98d0-3c15c2c6caf6'
ACCESS_TOKEN = 'access_token'
REFRESH_TOKEN = 'refresh_token'
EXPIRES_TIME = 36000


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
    response = __post_request(dhis2_config.DHIS2_STATIC_URLS.get(dhis2_config.OAUTH2_TOKEN), body,
                              (OAUTH2_UID, OAUTH2_SECRET), HEADER_OAUTH)
    json_data = json.loads(response.text)
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
        print("hey ya")
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
