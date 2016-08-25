import datetime

from django.test import TestCase
from mock import patch

from dsd.models import Province, District, Facility
from dsd.service.organization_converter import convert_province_to_dict, convert_district_to_dict, \
    convert_facility_to_dict
from dsd.test.factories.district_factory import DistrictFactory
from dsd.test.factories.facility_factory import FacilityFactory
from dsd.test.factories.province_factory import ProvinceFactory
from dsd.test.helpers.fake_date import FakeDate


class OrganizationConverterTest(TestCase):
    @patch('dsd.util.id_generator.generate_id')
    def test_should_convert_province_to_json(self, mock_generate_id):
        expected_province_dict = {'id': '12345678901',
                                  'name': 'MANICA',
                                  'shortName': 'MANICA',
                                  'openingDate': '2016-08-15',
                                  'description': 'province 1',
                                  'userCreation': 0,
                                  'state': 1,
                                  'parent': {'id': '00000000000'}}

        mock_generate_id.return_value = '12345678901'
        ProvinceFactory(province_name='MANICA', description='province 1', data_creation=datetime.date(2016, 8, 15))

        province = Province.objects.first()
        _, province_dict = convert_province_to_dict(province, '00000000000')

        self.assertEqual(province_dict, expected_province_dict)

    @patch('dsd.util.id_generator.generate_id')
    def test_should_convert_district_to_json(self, mock_generate_id):
        expected_district_dict = {'id': '98765432109',
                                  'name': 'MACOMIA',
                                  'shortName': 'MACOMIA',
                                  'openingDate': '2016-08-30',
                                  'description': 'district 1',
                                  'userCreation': 0,
                                  'state': 1,
                                  'parent': {'id': '12345678901'}}

        mock_generate_id.return_value = '98765432109'
        DistrictFactory(district_name='MACOMIA', description='district 1', data_creation=datetime.date(2016, 8, 30))

        district = District.objects.first()
        _, actual_district_dict = convert_district_to_dict(district, '12345678901')

        self.assertEqual(actual_district_dict, expected_district_dict)

    @patch('datetime.date', FakeDate)
    @patch('dsd.util.id_generator.generate_id')
    def test_should_convert_facility_to_json(self, mock_generate_id):
        expected_facility_dict = {'id': '98765432109',
                                  'name': 'DESCONHECIDO',
                                  'shortName': 'DESCONHECIDO',
                                  'openingDate': '2016-08-25',
                                  'latitude': '-17.15',
                                  'longitude': '35.74',
                                  'code_us': '797',
                                  'sorting_us': 'HEALTH POST',
                                  'level_us': 'LEVEL 1',
                                  'fea_us': '',
                                  'province_capital_dist': None,
                                  'device_serial': '356670060320751',
                                  'sim_number': '258823197418',
                                  'sim_serial': '8925801150348700919',
                                  'device_number': '97',
                                  'state': 1,
                                  'person_contact_opt': None,
                                  'phone_contact_opt': None,
                                  'sim_number_opt': None,
                                  'sim_serial_opt': None,
                                  'mac_number': '74:ba:db:20:a6:44',
                                  'device_serial_opt': '356670060276714',
                                  'parent': {'id': '12345678901'}}

        mock_generate_id.return_value = '98765432109'
        FacilityFactory(facility_name='DESCONHECIDO', sim_number='258823197418', sim_serial='8925801150348700919',
                        latitude='-17.15', longitude='35.74', mac_number='74:ba:db:20:a6:44',
                        device_serial_opt='356670060276714', device_serial='356670060320751', device_number='97')

        facility = Facility.objects.first()
        actual_facility_dict = convert_facility_to_dict(facility, '12345678901')

        self.assertEqual(actual_facility_dict, expected_facility_dict)
