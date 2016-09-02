import datetime
import uuid

from django.test import TestCase
from django.test import override_settings
from mock import MagicMock, call, patch
from rest_framework.status import HTTP_201_CREATED

from dsd.models.moh import MoH
from dsd.models.remote.bes_middleware_core import BesMiddlewareCore
from dsd.repositories import dhis2_remote_repository
from dsd.repositories.dhis2_remote_repository import *
from dsd.repositories.request_template.add_element_template import AddElementRequestTemplate
from dsd.services import dhis2_remote_service
from dsd.services.dhis2_remote_service import post_organization_units, post_elements, \
    build_data_set_request_body_as_dict, build_data_element_values_request_body_as_dict, \
    build_category_options_request_body_as_dict, build_categories_request_body_as_dict, \
    build_category_combinations_request_body_as_dict
from dsd.test.factories.category_combination_factory import CategoryCombinationFactory
from dsd.test.factories.category_factory import CategoryFactory
from dsd.test.factories.category_option_factory import CategoryOptionFactory
from dsd.test.factories.district_factory import DistrictFactory
from dsd.test.factories.element_factory import ElementFactory
from dsd.test.factories.facility_factory import FacilityFactory
from dsd.test.factories.province_factory import ProvinceFactory
from dsd.test.helpers.fake_date import FakeDate
from dsd.util.id_generator import generate_id


class DHIS2RemoteServiceTest(TestCase):
    def setUp(self):
        self.empty_request_body_dict = {}

    @patch('datetime.date', FakeDate)
    @patch('dsd.util.id_generator.generate_id')
    @patch('dsd.repositories.dhis2_remote_repository.get_access_token')
    @patch('requests.post')
    @override_settings(DHIS2_SSL_VERIFY=False)
    def test_should_post_organization_units(self, mock_post, mock_get_access_token, mock_generate_id):
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

        requests.post.assert_has_calls([call(url=dhis2_config.DHIS2_URLS.get(dhis2_config.KEY_POST_ORGANIZATION_UNIT),
                                             headers=get_oauth_header(),
                                             verify=settings.DHIS2_SSL_VERIFY,
                                             data=json.dumps(organization_unit_list[0])
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

        requests.post.assert_called_once_with(url=dhis2_config.DHIS2_URLS.get(dhis2_config.KEY_POST_ELEMENT),
                                              headers=HEADER_DHIS2,
                                              verify=settings.DHIS2_SSL_VERIFY,
                                              data=json.dumps(request_body_dict))

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('dsd.services.dhis2_remote_service.build_category_options_request_body_as_dict')
    @patch('dsd.repositories.dhis2_remote_repository.post_category_options')
    def test_should_post_category_options(self, mock_post_category_options,
                                          mock_build_category_options_request_body_as_dict):
        category_option = CategoryOptionFactory()
        mock_post_category_options.return_value = MagicMock(status_code=HTTP_201_CREATED)
        mock_build_category_options_request_body_as_dict.return_value = self.empty_request_body_dict

        dhis2_remote_service.post_category_options()

        mock_build_category_options_request_body_as_dict.assert_called_once_with(category_option)
        dhis2_remote_repository.post_category_options.assert_called_once_with(json.dumps(self.empty_request_body_dict))

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('dsd.services.dhis2_remote_service.build_categories_request_body_as_dict')
    @patch('dsd.repositories.dhis2_remote_repository.post_categories')
    def test_should_post_category_options(self, mock_post_categories,
                                          mock_build_categories_request_body_as_dict):
        category = CategoryFactory()

        mock_post_categories.return_value = MagicMock(status_code=HTTP_201_CREATED)
        mock_build_categories_request_body_as_dict.return_value = self.empty_request_body_dict

        dhis2_remote_service.post_categories()

        mock_build_categories_request_body_as_dict.assert_called_once_with(category)
        dhis2_remote_repository.post_categories.assert_called_once_with(json.dumps(self.empty_request_body_dict))

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('dsd.services.dhis2_remote_service.build_category_combinations_request_body_as_dict')
    @patch('dsd.repositories.dhis2_remote_repository.post_category_combinations')
    def test_should_post_category_combinations(self, mock_post_category_combinations,
                                          mock_build_category_combinations_request_body_as_dict):
        category_combination = CategoryCombinationFactory()

        mock_post_category_combinations.return_value = MagicMock(status_code=HTTP_201_CREATED)
        mock_build_category_combinations_request_body_as_dict.return_value = self.empty_request_body_dict

        dhis2_remote_service.post_category_combinations()

        mock_build_category_combinations_request_body_as_dict.assert_called_once_with(category_combination)
        dhis2_remote_repository.post_category_combinations.assert_called_once_with(json.dumps(self.empty_request_body_dict))

    def test_should_build_post_element_value_as_dict(self):
        id_test = generate_id()
        id_test2 = generate_id()
        device_serial = '353288063681856'
        uid = '8dd73ldj0ld'
        name = 'cases_nv_measles'
        name2 = 'cases_rabies'
        ElementFactory(name=name, id=id_test)
        ElementFactory(name=name2, id=id_test2)
        FacilityFactory(device_serial=device_serial, uid=uid)
        bes_middleware_core = BesMiddlewareCore(cases_rabies=2, cases_nv_measles=5, device_id=device_serial)
        result = build_data_element_values_request_body_as_dict(bes_middleware_core)
        self.assertEqual(result.get('orgUnit'), uid)
        self.assertEqual(len(result.get('dataValues')), 2)
        self.assertEqual(result.get('dataValues')[0].get('dataElement'), id_test)
        self.assertEqual(result.get('dataValues')[0].get('value'), 5)
        self.assertEqual(result.get('dataValues')[1].get('dataElement'), id_test2)
        self.assertEqual(result.get('dataValues')[1].get('value'), 2)

    def test_should_build_data_set_request_body_as_dict(self):
        facility1 = FacilityFactory()
        facility2 = FacilityFactory()

        element1 = ElementFactory(id=generate_id())
        element2 = ElementFactory(id=generate_id())

        request_body_dict = build_data_set_request_body_as_dict()

        self.assertEqual(len(request_body_dict.get('dataElements')), 2)
        self.assertEqual(request_body_dict.get('dataElements')[0].get('id'), element1.id)
        self.assertEqual(request_body_dict.get('dataElements')[1].get('id'), element2.id)
        self.assertEqual(request_body_dict.get('name'), dhis2_config.DATA_SET_NAME)
        self.assertEqual(request_body_dict.get('shortName'), dhis2_config.DATA_SET_NAME)

        self.assertEqual(len(request_body_dict.get('organisationUnits')), 2)
        self.assertEqual(request_body_dict.get('organisationUnits')[0].get('id'), facility1.uid)
        self.assertEqual(request_body_dict.get('organisationUnits')[1].get('id'), facility2.uid)

    def test_should_build_category_options_request_body_as_dict(self):
        option_id = generate_id()
        option_name = '5 anos'

        facility1 = FacilityFactory(uid=generate_id(), facility_name='CENTRO DE SAUDE DE CHINETE')
        facility2 = FacilityFactory(uid=generate_id(), facility_name='HOSPITAL DISTRITAL DE MACOMIA')

        request_body_dict = build_category_options_request_body_as_dict(
            CategoryOptionFactory(id=option_id, name=option_name))

        self.assertEqual(request_body_dict.get('id'), option_id)
        self.assertEqual(request_body_dict.get('name'), option_name)
        self.assertEqual(len(request_body_dict.get('organisationUnits')), 2)
        self.assertEqual(request_body_dict.get('organisationUnits')[0].get('id'), facility1.uid)
        self.assertEqual(request_body_dict.get('organisationUnits')[1].get('id'), facility2.uid)

    def test_should_build_categories_request_body_as_dict(self):
        category_id = generate_id()
        category_name = 'patient statistics'

        option_id1 = generate_id()
        option_id2 = generate_id()
        option_name1 = '5 anos'
        option_name2 = '5-14 anos'
        category_options1 = CategoryOptionFactory(id=option_id1, name=option_name1)
        category_options2 = CategoryOptionFactory(id=option_id2, name=option_name2)

        request_body_dict = build_categories_request_body_as_dict(
            CategoryFactory(id=category_id, name=category_name,
                            category_options=(category_options1, category_options2)))

        self.assertEqual(request_body_dict.get('id'), category_id)
        self.assertEqual(request_body_dict.get('name'), category_name)
        self.assertEqual(len(request_body_dict.get('categoryOptions')), 2)
        self.assertEqual(request_body_dict.get('categoryOptions')[0].get('id'), category_options1.id)
        self.assertEqual(request_body_dict.get('categoryOptions')[1].get('id'), category_options2.id)

    def test_should_build_category_combinations_request_body_as_dict(self):
        category_name = 'patient statistics'

        option_id1 = generate_id()
        option_id2 = generate_id()
        option_name1 = '5 anos'
        option_name2 = '5-14 anos'
        category_options1 = CategoryOptionFactory(id=option_id1, name=option_name1)
        category_options2 = CategoryOptionFactory(id=option_id2, name=option_name2)

        category1 = CategoryFactory(id=generate_id(), name=category_name,
                                    category_options=(category_options1, category_options2))
        category2 = CategoryFactory(id=generate_id(), name=category_name, category_options=(category_options1,))

        combination_id = generate_id()
        combination_name = 'meningte stat'
        request_body_dict = build_category_combinations_request_body_as_dict(
            CategoryCombinationFactory(id=combination_id, name=combination_name, categories=(category1, category2)))

        self.assertEqual(request_body_dict.get('id'), combination_id)
        self.assertEqual(request_body_dict.get('name'), combination_name)
        self.assertEqual(len(request_body_dict.get('categories')), 2)
        self.assertEqual(request_body_dict.get('categories')[0].get('id'), category1.id)
        self.assertEqual(request_body_dict.get('categories')[1].get('id'), category2.id)
