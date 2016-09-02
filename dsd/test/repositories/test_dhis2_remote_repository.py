import uuid

from django.test import TestCase
from django.test import override_settings
from mock import MagicMock, patch
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from dsd.repositories.dhis2_remote_repository import *


class DHIS2RemoteRepositoryTest(TestCase):
    def setUp(self):
        self.empty_request_body = json.dumps({})

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('dsd.repositories.dhis2_remote_repository.get_access_token')
    @patch('requests.post')
    def test_should_post_date_sets(self, mock_post, mock_get_access_token):
        mock_post.return_value = MagicMock(status_code=HTTP_201_CREATED)
        mock_get_access_token.return_value = uuid.uuid4()
        HEADER_DHIS2 = get_oauth_header()

        post_data_set(self.empty_request_body)

        requests.post.assert_called_once_with(url=dhis2_config.DHIS2_URLS.get(dhis2_config.KEY_ADD_DATA_SET),
                                              headers=HEADER_DHIS2,
                                              verify=settings.DHIS2_SSL_VERIFY,
                                              data=self.empty_request_body)

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('requests.post', side_effect=ConnectionError())
    def test_should_raise_remote_request_exception_when_add_organization_unit_connection_error(self, _):
        with self.assertRaises(RemoteRequestException):
            post_organization_unit(request_body=self.empty_request_body)

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('dsd.repositories.dhis2_remote_repository.get_access_token')
    @patch('requests.post')
    def test_should_post_single_attribute(self, mock_post, mock_get_access_token):
        mock_post.return_value = MagicMock(status_code=HTTP_200_OK)
        mock_get_access_token.return_value = uuid.uuid4()
        response = post_attribute(request_body=self.empty_request_body)
        HEADER_DHIS2 = get_oauth_header()
        self.assertEqual(response.status_code, HTTP_200_OK)
        requests.post.assert_called_once_with(url=dhis2_config.DHIS2_URLS.get(dhis2_config.KEY_ADD_ATTRIBUTE),
                                              headers=HEADER_DHIS2,
                                              verify=settings.DHIS2_SSL_VERIFY,
                                              data=self.empty_request_body)

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('dsd.repositories.dhis2_remote_repository.get_access_token')
    @patch('requests.post')
    def test_should_post_data_set_elements(self, mock_post, mock_get_access_token):
        mock_get_access_token.return_value = uuid.uuid4()
        mock_post.return_value = MagicMock(status_code=HTTP_201_CREATED)
        response = post_data_elements_value(request_body=self.empty_request_body)
        HEADER_DHIS2 = get_oauth_header()
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        requests.post.assert_called_once_with(url=dhis2_config.DHIS2_URLS.get(dhis2_config.KEY_ADD_DATA_SET_ELEMENTS),
                                              headers=HEADER_DHIS2,
                                              verify=settings.DHIS2_SSL_VERIFY,
                                              data=self.empty_request_body)

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('dsd.repositories.dhis2_remote_repository.get_access_token')
    @patch('requests.post')
    def test_should_post_date_sets(self, mock_post, mock_get_access_token):
        mock_post.return_value = MagicMock(status_code=HTTP_201_CREATED)
        mock_get_access_token.return_value = uuid.uuid4()
        HEADER_DHIS2 = get_oauth_header()
        post_data_set(self.empty_request_body)
        requests.post.assert_called_once_with(url=dhis2_config.DHIS2_URLS.get(dhis2_config.KEY_ADD_DATA_SET),
                                              headers=HEADER_DHIS2,
                                              verify=settings.DHIS2_SSL_VERIFY,
                                              data=self.empty_request_body)
