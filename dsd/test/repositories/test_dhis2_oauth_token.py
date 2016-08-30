import uuid

from django.test import TestCase
from django.test import override_settings
from mock import patch

from dsd.repositories.dhis2_oauth_token import *
from dsd.test.helpers.fake_cache import FakeCache


class DHIS2OauthTokenTest(TestCase):
    @patch('requests.post')
    @patch('django.core.cache',FakeCache)
    @override_settings(DHIS2_SSL_VERIFY=False)
    def test_should_return_refresh_token(self, mock_post):
        BODY = {'grant_type': 'password', 'username': 'admin', 'password': 'district'}
        mock_post.return_value.text = json.dumps({REFRESH_TOKEN:str(uuid.uuid4())})
        set_refresh_token()
        requests.post.assert_called_once_with(url=dhis2_config.DHIS2_URLS.get(dhis2_config.OAUTH2_TOKEN),
                                              headers=HEADER_OAUTH,
                                              auth= (OAUTH2_UID, OAUTH2_SECRET),
                                              verify=settings.DHIS2_SSL_VERIFY,
                                              data=BODY)
