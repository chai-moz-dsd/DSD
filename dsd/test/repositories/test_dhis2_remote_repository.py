import datetime
import uuid

from django.test import TestCase
from django.test import override_settings
from mock import MagicMock, call, patch
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from dsd.models.moh import MoH
from dsd.repositories.dhis2_remote_repository import *
from dsd.repositories.request_template.add_attribute_template import AddAttributeRequestTemplate
from dsd.services.data_set_service import build_data_set_element_request_body_as_json
from dsd.test.factories.data_set_element_factory import DataSetElementFactory
from dsd.test.factories.district_factory import DistrictFactory
from dsd.test.factories.facility_factory import FacilityFactory
from dsd.test.factories.province_factory import ProvinceFactory
from dsd.test.helpers.fake_date import FakeDate

add_attribute_request_body = AddAttributeRequestTemplate().build(uid="MKoA22RCFfC", code='Sim number',
                                                                 valueType='NUMBER',
                                                                 orgUnitAttr=True,
                                                                 name='Sim number')


class DHIS2RemoteRepositoryTest(TestCase):
    @patch('datetime.date', FakeDate)
    @patch('dsd.util.id_generator.generate_id')
    @patch('dsd.repositories.dhis2_remote_repository.get_access_token')
    @patch('requests.post')
    @override_settings(DHIS2_SSL_VERIFY=False)
    def test_should_add_organization_unit(self, mock_post, mock_get_access_token, mock_generate_id):
        mock_generate_id.side_effect = ['00000000000', '11111111111', '22222222222', '33333333333', '44444444444',
                                        '55555555555', '66666666666']

        province_1 = ProvinceFactory(province_name='NAMPULA', description='province 1', state=0,
                                     data_creation=datetime.date(2016, 8, 15))
        province_2 = ProvinceFactory(province_name='TETE', description='province 2', state=1,
                                     data_creation=datetime.date(2016, 8, 15))

        district_1 = DistrictFactory(district_name='MACOMIA', description='district 1', state=0,
                                     data_creation=datetime.date(2016, 8, 30), province=province_1)
        district_2 = DistrictFactory(district_name='BALAMA', description='district 2', state=1,
                                     data_creation=datetime.date(2016, 8, 30), province=province_2)

        FacilityFactory(facility_name='DESCONHECIDO', district=district_1, province=province_1)
        FacilityFactory(facility_name='POSTO DE SAUDE', district=district_2, province=province_2)

        add_organization_unit_request_body = MoH().get_organization_as_dict()
        mock_post.return_value = MagicMock(status_code=HTTP_201_CREATED)
        mock_get_access_token.return_value = uuid.uuid4()
        response = add_organization_unit(request_body=add_organization_unit_request_body)
        HEADER_DHIS2 = get_oauth_header()
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        requests.post.assert_called_once_with(url=settings.DHIS2_URLS.get(settings.KEY_ADD_ORGANIZATION_UNIT),
                                              headers=HEADER_DHIS2,
                                              verify=settings.DHIS2_SSL_VERIFY,
                                              data=add_organization_unit_request_body)

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('requests.post', side_effect=ConnectionError())
    def test_should_raise_remote_request_exception_when_add_organization_unit_connection_error(self, _):
        with self.assertRaises(RemoteRequestException):
            add_organization_unit(request_body=add_attribute_request_body)

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('dsd.repositories.dhis2_remote_repository.get_access_token')
    @patch('requests.post')
    def test_should_add_attribute(self, mock_post, mock_get_access_token):
        mock_post.return_value = MagicMock(status_code=HTTP_200_OK)
        mock_get_access_token.return_value = uuid.uuid4()
        response = add_attribute(request_body=add_attribute_request_body)
        HEADER_DHIS2 = get_oauth_header()
        self.assertEqual(response.status_code, HTTP_200_OK)
        requests.post.assert_called_once_with(url=settings.DHIS2_URLS.get(settings.KEY_ADD_ATTRIBUTE),
                                              headers=HEADER_DHIS2,
                                              verify=settings.DHIS2_SSL_VERIFY,
                                              data=add_attribute_request_body)

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('dsd.repositories.dhis2_remote_repository.get_access_token')
    @patch('requests.post')
    def test_should_raise_remote_request_exception_when_add_attribute_connection_error(self, mock_post,
                                                                                       mock_get_access_token):
        mock_post.side_effect = ConnectionError()
        with self.assertRaises(RemoteRequestException):
            mock_get_access_token.return_value = uuid.uuid4()
            HEADER_DHIS2 = get_oauth_header()
            add_attribute(request_body=add_attribute_request_body)
            requests.post.assert_has_calls([call(url=settings.DHIS2_URLS.get(settings.KEY_ADD_ATTRIBUTE_TO_SCHEMAS),
                                                 headers=HEADER_DHIS2,
                                                 verify=settings.DHIS2_SSL_VERIFY,
                                                 data=add_attribute_request_body
                                                 )], any_order=True)

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('dsd.repositories.dhis2_remote_repository.get_access_token')
    @patch('requests.post')
    def test_should_add_attribute_to_schemas(self, mock_post, mock_get_access_token):
        mock_post.return_value = MagicMock(status_code=HTTP_201_CREATED)
        mock_get_access_token.return_value = uuid.uuid4()
        response = add_attribute_to_schemas(request_body=add_attribute_request_body)
        HEADER_DHIS2 = get_oauth_header()
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        requests.post.assert_called_once_with(url=settings.DHIS2_URLS.get(settings.KEY_ADD_ATTRIBUTE_TO_SCHEMAS),
                                              headers=HEADER_DHIS2,
                                              verify=settings.DHIS2_SSL_VERIFY,
                                              data=add_attribute_request_body)

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('requests.post', side_effect=ConnectionError())
    def test_should_raise_remote_request_exception_when_add_attribute_to_schemas_connection_error(self, _):
        with self.assertRaises(RemoteRequestException):
            add_attribute_to_schemas(request_body=add_attribute_request_body)

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('dsd.repositories.dhis2_remote_repository.get_access_token')
    @patch('requests.post')
    def test_should_add_data_set_elements(self, mock_post, mock_get_access_token):
        mock_post.return_value = MagicMock(status_code=HTTP_201_CREATED)
        data_set_element_list = [DataSetElementFactory(), DataSetElementFactory(), DataSetElementFactory()]
        request_body = build_data_set_element_request_body_as_json(data_set_element_list)
        mock_get_access_token.return_value = uuid.uuid4()
        response = add_data_set_elements(request_body=request_body)
        HEADER_DHIS2 = get_oauth_header()
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        requests.post.assert_called_once_with(url=settings.DHIS2_URLS.get(settings.KEY_ADD_DATA_SET_ELEMENTS),
                                              headers=HEADER_DHIS2,
                                              verify=settings.DHIS2_SSL_VERIFY,
                                              data=request_body)
