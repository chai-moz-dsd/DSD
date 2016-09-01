import uuid

from django.test import TestCase
from django.test import override_settings
from mock import MagicMock, patch
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from dsd.models import BesMiddlewareCore
from dsd.repositories.dhis2_remote_repository import *
from dsd.repositories.request_template.add_attribute_template import AddAttributeRequestTemplate
from dsd.services.bes_middleware_core_service import build_post_data_set_request_body_as_dict
from dsd.test.factories.element_factory import ElementFactory
from dsd.test.factories.facility_factory import FacilityFactory
from dsd.util.id_generator import generate_id

add_attribute_request_body = AddAttributeRequestTemplate().build(uid="MKoA22RCFfC", code='Sim number',
                                                                 value_type='NUMBER',
                                                                 org_unit_attr=True,
                                                                 name='Sim number')


class DHIS2RemoteRepositoryTest(TestCase):
    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('requests.post', side_effect=ConnectionError())
    def test_should_raise_remote_request_exception_when_add_organization_unit_connection_error(self, _):
        with self.assertRaises(RemoteRequestException):
            add_organization_unit(request_body=add_attribute_request_body)

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('dsd.repositories.dhis2_remote_repository.get_access_token')
    @patch('requests.post')
    def test_should_post_single_attribute(self, mock_post, mock_get_access_token):
        mock_post.return_value = MagicMock(status_code=HTTP_200_OK)
        mock_get_access_token.return_value = uuid.uuid4()
        response = add_attribute(request_body=add_attribute_request_body)
        HEADER_DHIS2 = get_oauth_header()
        self.assertEqual(response.status_code, HTTP_200_OK)
        requests.post.assert_called_once_with(url=dhis2_config.DHIS2_URLS.get(dhis2_config.KEY_ADD_ATTRIBUTE),
                                              headers=HEADER_DHIS2,
                                              verify=settings.DHIS2_SSL_VERIFY,
                                              data=add_attribute_request_body)

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('dsd.repositories.dhis2_remote_repository.get_access_token')
    @patch('requests.post')
    def test_should_post_data_set_elements(self, mock_post, mock_get_access_token):
        mock_post.return_value = MagicMock(status_code=HTTP_201_CREATED)
        id_test = generate_id()
        id_test2 = generate_id()
        device_serial = '353288063681856'
        uid = '8dd73ldj0ld'
        name = 'cases_nv_measles'
        name2 = 'cases_anger'
        ElementFactory(name=name, id=id_test)
        ElementFactory(name=name2, id=id_test2)
        FacilityFactory(device_serial=device_serial, uid=uid)
        bes_middleware_core = BesMiddlewareCore(cases_anger=2, cases_nv_measles=5, device_id=device_serial)

        request_body_dict = build_post_data_set_request_body_as_dict(bes_middleware_core)
        mock_get_access_token.return_value = uuid.uuid4()
        response = add_data_set_elements_value(request_body=json.dumps(request_body_dict))
        HEADER_DHIS2 = get_oauth_header()
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        requests.post.assert_called_once_with(url=dhis2_config.DHIS2_URLS.get(dhis2_config.KEY_ADD_DATA_SET_ELEMENTS),
                                              headers=HEADER_DHIS2,
                                              verify=settings.DHIS2_SSL_VERIFY,
                                              data=json.dumps(request_body_dict))

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('dsd.repositories.dhis2_remote_repository.get_access_token')
    @patch('requests.post')
    def test_should_post_date_sets(self, mock_post, mock_get_access_token):
        request_body = {"dataElements": [{id: "sTktPCnAYpw"}],
                        "expiryDays": 0,
                        "fieldCombinationRequired": False,
                        "indicators": [],
                        "mobile": False,
                        "name": "",
                        "openFuturePeriods": 0,
                        "organisationUnits": [{"id": "b5d194d5a7d"}, {"id": "8ad2dca6fe8"}, {"id": "6844c842399"},
                                              {"id": "a7a2ae57e12"}],
                        "periodType": "Weekly",
                        "shortName": "test set",
                        "timelyDays": 15,
                        }
        mock_post.return_value = MagicMock(status_code=HTTP_201_CREATED)
        mock_get_access_token.return_value = uuid.uuid4()
        HEADER_DHIS2 = get_oauth_header()

        post_data_set(request_body)

        requests.post.assert_called_once_with(url=dhis2_config.DHIS2_URLS.get(dhis2_config.KEY_ADD_DATA_SET),
                                              headers=HEADER_DHIS2,
                                              verify=settings.DHIS2_SSL_VERIFY,
                                              data=request_body)
