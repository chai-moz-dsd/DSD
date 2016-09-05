import uuid

from django.test import TestCase
from django.test import override_settings
from mock import patch

from dsd.repositories.dhis2_oauth_token import *


class DHIS2OauthTokenTest(TestCase):
    @patch('django.core.cache.cache.set')
    @patch('requests.post')
    @patch('dsd.repositories.dhis2_oauth_token.USERNAME', 'username')
    @patch('dsd.repositories.dhis2_oauth_token.PASSWORD', 'password')
    @patch('dsd.repositories.dhis2_oauth_token.OAUTH2_UID', 'uid')
    @patch('dsd.repositories.dhis2_oauth_token.OAUTH2_SECRET', 'secret')
    @override_settings(DHIS2_SSL_VERIFY=False)
    def test_should_return_refresh_token(self, mock_post, mock_set):
        mock_post.return_value.text = json.dumps({REFRESH_TOKEN: str(uuid.uuid4())})
        mock_set.return_value = True
        body = {'grant_type': 'password', 'username': 'username', 'password': 'password'}
        set_refresh_token()
        requests.post.assert_called_once_with(url=dhis2_config.DHIS2_STATIC_URLS.get(dhis2_config.OAUTH2_TOKEN),
                                              headers=HEADER_OAUTH,
                                              auth=('uid', 'secret'),
                                              verify=settings.DHIS2_SSL_VERIFY,
                                              data=body)

    @patch('dsd.repositories.dhis2_oauth_token.OAUTH2_UID', 'uid')
    @patch('dsd.repositories.dhis2_oauth_token.OAUTH2_SECRET', 'secret')
    @patch('django.core.cache.cache.get')
    @patch('django.core.cache.cache.set')
    @patch('requests.post')
    @override_settings(DHIS2_SSL_VERIFY=False)
    def test_should_return_access_token(self, mock_post, mock_set, mock_get):
        mock_get.return_value = "929a3cec-16b5-47bc-87c7-e90e6fbc8207"
        mock_set.return_value = True
        body = {'grant_type': "refresh_token", "refresh_token": "929a3cec-16b5-47bc-87c7-e90e6fbc8207"}
        mock_post.return_value.text = json.dumps({ACCESS_TOKEN: str(uuid.uuid4())})
        set_access_token()
        requests.post.assert_called_once_with(url=dhis2_config.DHIS2_STATIC_URLS.get(dhis2_config.OAUTH2_TOKEN),
                                              data=body,
                                              auth=('uid', 'secret'),
                                              headers=HEADER_OAUTH,
                                              verify=settings.DHIS2_SSL_VERIFY)

    @patch('dsd.repositories.dhis2_oauth_token.set_refresh_token')
    @patch('dsd.repositories.dhis2_oauth_token.set_access_token')
    @patch('requests.post')
    @patch('dsd.repositories.dhis2_oauth_token.OAUTH2_UID', 'uid')
    @patch('dsd.repositories.dhis2_oauth_token.OAUTH2_SECRET', 'secret')
    @patch('dsd.repositories.dhis2_oauth_token.USERNAME', 'username')
    @patch('dsd.repositories.dhis2_oauth_token.PASSWORD', 'password')
    def test_should_create_oauth_token(self, mock_post, mock_set_access_token, mock_set_refresh_token):
        mock_set_access_token.return_value = True
        mock_set_refresh_token.return_value = True
        body = {
            'name': 'DSD Client',
            'cid': 'uid',
            'secret': 'secret',
            'grantTypes': ['password', 'refresh_token', 'authorization_code']
        }
        header = {'Content-Type': 'application/json'}
        mock_post.return_value.text = json.dumps({})
        create_oauth()
        requests.post.assert_called_once_with(url=dhis2_config.DHIS2_STATIC_URLS.get(dhis2_config.OAUTH2_CREATE),
                                              data= json.dumps(body),
                                              auth=('username', 'password'),
                                              headers=header,
                                              verify=settings.DHIS2_SSL_VERIFY)

