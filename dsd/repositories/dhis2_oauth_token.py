import requests
import json
from django.conf import settings
from django.core.cache import cache
from dsd.exceptions.remote_request_exception import RemoteRequestException

HEADER_OAUTH = {'Accept': 'application/json'}
USERNAME = 'admin'
PASSWORD = 'district'
OAUTH2_UID = 'moh'
OAUTH2_SECRET = '1e6db50c-0fee-11e5-98d0-3c15c2c6caf6'
ACCESS_TOKEN = 'access_token'
REFRESH_TOKEN = 'refresh_token'

# EXPIRES_TIME shoud smaller than 43200 seconds
EXPIRES_TIME = 36000


def get_access_token():
    if cache.get(ACCESS_TOKEN) is not None:
        return cache.get(ACCESS_TOKEN)
    if cache.get(REFRESH_TOKEN) is None:
        set_refresh_token()
    refresh_token = cache.get(REFRESH_TOKEN)
    BODY = {'grant_type': REFRESH_TOKEN, REFRESH_TOKEN: refresh_token}
    json_data = __post_request(settings.DHIS2_URLS.get(settings.OAUTH2_TOKEN), BODY, (OAUTH2_UID, OAUTH2_SECRET))
    cache.set(ACCESS_TOKEN, json_data[ACCESS_TOKEN], EXPIRES_TIME)
    return cache.get(ACCESS_TOKEN)


def set_refresh_token():
    BODY = {'grant_type': 'password', 'username': USERNAME, 'password': PASSWORD}
    json_data = __post_request(settings.DHIS2_URLS.get(settings.OAUTH2_TOKEN), BODY, (OAUTH2_UID, OAUTH2_SECRET))
    cache.set(REFRESH_TOKEN, json_data[REFRESH_TOKEN], EXPIRES_TIME)


def __post_request(url, data, auth):
    try:
        response = requests.post(url=url,
                                 data=data,
                                 auth=auth,
                                 headers=HEADER_OAUTH,
                                 verify=settings.DHIS2_SSL_VERIFY)
        json_data = json.loads(response.text)
        return json_data
    except ConnectionError:
        raise RemoteRequestException()
