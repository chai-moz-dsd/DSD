from unittest import TestCase

import requests
from django.conf import settings
from django.test import override_settings
from mock import MagicMock, call
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from dsd.exceptions.remote_request_exception import RemoteRequestException
from dsd.repositories.dhis2_remote_repository import add_attribute, HEADER_DHIS2, add_attribute_to_schemas
from dsd.repositories.request_template.add_attribute_template import AddAttributeRequestTemplate

request_body = AddAttributeRequestTemplate().build(code=1, valueType='NUMBER', organisationUnitAttribute=True,
                                                   name='Sim number')


class DHIS2RemoteRepositoryTest(TestCase):
    @override_settings(DHIS2_SSL_VERIFY=False)
    def test_should_add_attribute(self):
        requests.post = MagicMock(return_value=MagicMock(status_code=HTTP_200_OK))
        response = add_attribute(request_body=request_body)
        self.assertEqual(response.status_code, HTTP_200_OK)
        requests.post.assert_called_once_with(url=settings.DHIS2_URLS.get(settings.KEY_ADD_ATTRIBUTE),
                                              headers=HEADER_DHIS2,
                                              verify=settings.DHIS2_SSL_VERIFY,
                                              data=request_body)

    @override_settings(DHIS2_SSL_VERIFY=False)
    def test_should_raise_remote_request_exception_when_add_attribute_connection_error(self):
        requests.post.side_effect = ConnectionError()
        with self.assertRaises(RemoteRequestException):
            add_attribute(request_body=request_body)
        requests.post.assert_has_calls([call(url=settings.DHIS2_URLS.get(settings.KEY_ADD_ATTRIBUTE_TO_SCHEMAS),
                                             headers=HEADER_DHIS2,
                                             verify=settings.DHIS2_SSL_VERIFY,
                                             data=request_body
                                             )], any_order=True)

    @override_settings(DHIS2_SSL_VERIFY=False)
    def test_should_add_attribute_to_schemas(self):
        requests.post = MagicMock(return_value=MagicMock(status_code=HTTP_201_CREATED))
        response = add_attribute_to_schemas(request_body=request_body)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        requests.post.assert_called_once_with(url=settings.DHIS2_URLS.get(settings.KEY_ADD_ATTRIBUTE_TO_SCHEMAS),
                                              headers=HEADER_DHIS2,
                                              verify=settings.DHIS2_SSL_VERIFY,
                                              data=request_body)

    @override_settings(DHIS2_SSL_VERIFY=False)
    def test_should_raise_remote_request_exception_when_add_attribute_to_schemas_connection_error(self):
        requests.post.side_effect = ConnectionError()
        with self.assertRaises(RemoteRequestException):
            add_attribute_to_schemas(request_body=request_body)
