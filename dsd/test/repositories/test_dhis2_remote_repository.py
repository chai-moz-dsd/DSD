import json
import uuid

from django.test import TestCase
from django.test import override_settings
from mock import MagicMock, patch
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from dsd.repositories import dhis2_remote_repository
from dsd.repositories.dhis2_remote_repository import *


class DHIS2RemoteRepositoryTest(TestCase):
    def setUp(self):
        self.empty_request_body = json.dumps({})

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('requests.post')
    def test_should_post_category_combinations(self, mock_post):
        mock_post.return_value = MagicMock(status_code=HTTP_201_CREATED)

        post_category_combinations(self.empty_request_body)

        requests.post.assert_called_once_with(
            url=dhis2_config.DHIS2_STATIC_URLS.get(dhis2_config.KEY_POST_CATEGORY_COMBINATIONS),
            headers=dhis2_config.POST_HEADERS,
            auth=(settings.USERNAME, settings.PASSWORD),
            verify=settings.DHIS2_SSL_VERIFY,
            data=self.empty_request_body)

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('requests.post')
    def test_should_post_categories(self, mock_post):
        mock_post.return_value = MagicMock(status_code=HTTP_201_CREATED)

        post_categories(self.empty_request_body)

        requests.post.assert_called_once_with(url=dhis2_config.DHIS2_STATIC_URLS.get(dhis2_config.KEY_POST_CATEGORIES),
                                              headers=dhis2_config.POST_HEADERS,
                                              auth=(settings.USERNAME, settings.PASSWORD),
                                              verify=settings.DHIS2_SSL_VERIFY,
                                              data=self.empty_request_body)

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('requests.post')
    def test_should_post_category_options(self, mock_post):
        mock_post.return_value = MagicMock(status_code=HTTP_201_CREATED)

        post_category_options(self.empty_request_body)

        requests.post.assert_called_once_with(
            url=dhis2_config.DHIS2_STATIC_URLS.get(dhis2_config.KEY_POST_CATEGORY_OPTIONS),
            headers=dhis2_config.POST_HEADERS,
            auth=(settings.USERNAME, settings.PASSWORD),
            verify=settings.DHIS2_SSL_VERIFY,
            data=self.empty_request_body)

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('requests.post')
    def test_should_post_date_sets(self, mock_post):
        mock_post.return_value = MagicMock(status_code=HTTP_201_CREATED)

        post_data_set(self.empty_request_body)

        requests.post.assert_called_once_with(url=dhis2_config.DHIS2_STATIC_URLS.get(dhis2_config.KEY_POST_DATA_SET),
                                              headers=dhis2_config.POST_HEADERS,
                                              auth=(settings.USERNAME, settings.PASSWORD),
                                              verify=settings.DHIS2_SSL_VERIFY,
                                              data=self.empty_request_body)

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('requests.post', side_effect=ConnectionError())
    def test_should_raise_remote_request_exception_when_post_organization_unit_connection_error(self, _):
        with self.assertRaises(RemoteRequestException):
            post_organization_unit(request_body=self.empty_request_body)

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('requests.post')
    def test_should_post_single_attribute(self, mock_post):
        mock_post.return_value = MagicMock(status_code=HTTP_200_OK)
        response = post_attribute(request_body=self.empty_request_body)
        self.assertEqual(response.status_code, HTTP_200_OK)
        requests.post.assert_called_once_with(url=dhis2_config.DHIS2_STATIC_URLS.get(dhis2_config.KEY_POST_ATTRIBUTE),
                                              headers=dhis2_config.POST_HEADERS,
                                              auth=(settings.USERNAME, settings.PASSWORD),
                                              verify=settings.DHIS2_SSL_VERIFY,
                                              data=self.empty_request_body)

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('requests.post', side_effect=ConnectionError())
    def test_should_raise_remote_request_exception_when_post_single_attribute_connection_error(self, _):
        with self.assertRaises(RemoteRequestException):
            post_attribute(request_body=self.empty_request_body)

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('requests.post')
    def test_should_post_data_set_elements_value(self, mock_post):
        mock_post.return_value = MagicMock(status_code=HTTP_201_CREATED)
        response = post_data_elements_value(request_body=self.empty_request_body)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        requests.post.assert_called_once_with(
            url=dhis2_config.DHIS2_STATIC_URLS.get(dhis2_config.KEY_POST_DATA_SET_ELEMENTS),
            headers=dhis2_config.POST_HEADERS,
            auth=(settings.USERNAME, settings.PASSWORD),
            verify=settings.DHIS2_SSL_VERIFY,
            data=self.empty_request_body)

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('requests.post', side_effect=ConnectionError())
    def test_should_raise_remote_request_exception_when_post_date_set_elements_value_connection_error(self, _):
        with self.assertRaises(RemoteRequestException):
            post_data_elements_value(request_body=self.empty_request_body)

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('requests.post')
    def test_should_post_data_set(self, mock_post):
        mock_post.return_value = MagicMock(status_code=HTTP_201_CREATED)
        post_data_set(self.empty_request_body)
        requests.post.assert_called_once_with(url=dhis2_config.DHIS2_STATIC_URLS.get(dhis2_config.KEY_POST_DATA_SET),
                                              headers=dhis2_config.POST_HEADERS,
                                              auth=(settings.USERNAME, settings.PASSWORD),
                                              verify=settings.DHIS2_SSL_VERIFY,
                                              data=self.empty_request_body)

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('requests.post', side_effect=ConnectionError())
    def test_should_raise_remote_request_exception_when_post_date_set_connection_error(self, _):
        with self.assertRaises(RemoteRequestException):
            post_data_set(request_body=self.empty_request_body)

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('requests.get')
    def test_should_get_data_element_value_in_specific_period(self, mock_get):
        mock_get.return_value = MagicMock(status_code=HTTP_200_OK)

        query_params = 'dimension=dx:rf040c9a7ab.GRIMsGFQHUc&dimension=ou:MOH12345678&filter=pe:2016W23;2016W24;2016W25;2016W26'
        response = dhis2_remote_repository.get_data_element_values(query_params)
        self.assertEqual(response.status_code, HTTP_200_OK)
        url = '%s?%s' % (dhis2_config.DHIS2_STATIC_URLS.get(dhis2_config.KEY_GET_DATA_ELEMENT_VALUES), query_params)
        requests.get.assert_called_once_with(url=url,
                                             auth=(settings.USERNAME, settings.PASSWORD),
                                             verify=settings.DHIS2_SSL_VERIFY,
                                             headers=dhis2_config.POST_HEADERS)

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('requests.get')
    def test_should_get_default_customized_validation_rules(self,mock_get):
        mock_get.return_value = MagicMock(status_code=HTTP_200_OK)
        query_params = 'fields=id&fields=validationRuleGroups&filter=additionalRuleType:eq:Default'
        dhis2_remote_repository.get_validation_rules(query_params)

        url = '%s?%s' % (dhis2_config.DHIS2_STATIC_URLS.get(dhis2_config.KEY_GET_VALIDATION_RULES), query_params)
        requests.get.assert_called_once_with(url=url,
                                             auth=(settings.USERNAME, settings.PASSWORD),
                                             verify=settings.DHIS2_SSL_VERIFY,
                                             headers=dhis2_config.POST_HEADERS)



