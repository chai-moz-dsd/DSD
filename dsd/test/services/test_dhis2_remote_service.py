import datetime
import uuid

from django.test import TestCase
from django.test import override_settings
from mock import MagicMock, call, patch
from rest_framework.status import HTTP_201_CREATED

from dsd.models.moh import MoH
from dsd.repositories.dhis2_remote_repository import *
from dsd.repositories.request_template.add_attribute_template import AddAttributeRequestTemplate
from dsd.repositories.request_template.add_element_template import AddElementRequestTemplate
from dsd.services.dhis2_remote_service import post_organization_units, post_elements
from dsd.test.factories.district_factory import DistrictFactory
from dsd.test.factories.element_factory import ElementFactory
from dsd.test.factories.facility_factory import FacilityFactory
from dsd.test.factories.province_factory import ProvinceFactory
from dsd.test.helpers.fake_date import FakeDate

add_attribute_request_body = AddAttributeRequestTemplate().build(uid="MKoA22RCFfC", code='Sim number',
                                                                 value_type='NUMBER',
                                                                 org_unit_attr=True,
                                                                 name='Sim number')


class DHIS2RemoteRepositoryTest(TestCase):
    @patch('datetime.date', FakeDate)
    @patch('dsd.util.id_generator.generate_id')
    @patch('dsd.repositories.dhis2_remote_repository.get_access_token')
    @patch('requests.post')
    @override_settings(DHIS2_SSL_VERIFY=False)
    def should_post_organization_units(self, mock_post, mock_get_access_token, mock_generate_id):
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

        organization_unit_list = MoH().get_organization_as_list()

        mock_post.return_value = MagicMock(status_code=HTTP_201_CREATED)
        mock_get_access_token.return_value = uuid.uuid4()

        post_organization_units()

        requests.post.assert_has_calls([call(url=dhis2_config.DHIS2_URLS.get(dhis2_config.KEY_ADD_ORGANIZATION_UNIT),
                                             headers=get_oauth_header(),
                                             verify=settings.DHIS2_SSL_VERIFY,
                                             data=organization_unit_list
                                             )])

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('dsd.repositories.dhis2_remote_repository.get_access_token')
    @patch('requests.post')
    def test_should_post_elements(self, mock_post, mock_get_access_token):
        element = ElementFactory()

        request_body_dict = AddElementRequestTemplate().build(id=element.id,
                                                              code=element.code,
                                                              value_type=element.value_type,
                                                              short_name=element.short_name,
                                                              domain_type=element.domain_type,
                                                              category_combo=dhis2_config.CATEGORY_COMBO_ID,
                                                              aggregation_type=element.aggregation_type,
                                                              name=element.name)
        mock_post.return_value = MagicMock(status_code=HTTP_201_CREATED)
        mock_get_access_token.return_value = uuid.uuid4()
        HEADER_DHIS2 = get_oauth_header()

        post_elements()

        requests.post.assert_called_once_with(url=dhis2_config.DHIS2_URLS.get(dhis2_config.KEY_ADD_ELEMENT),
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
