import datetime

from django.test import TestCase
from mock import patch

from dsd.models import Province, District, Facility
from dsd.services.organization_service import convert_province_to_dict, convert_district_to_dict, \
    convert_facility_to_dict
from dsd.test.factories.district_factory import DistrictFactory
from dsd.test.factories.facility_factory import FacilityFactory
from dsd.test.factories.province_factory import ProvinceFactory
from dsd.test.helpers.fake_date import FakeDate


class OrganizationServiceTest(TestCase):
    def test_should_convert_province_to_json(self):
        expected_province_dict = {'id': '12345678901',
                                  'name': 'MANICA',
                                  'shortName': 'MANICA',
                                  'openingDate': '2016-08-15',
                                  'description': 'province 1',
                                  'attributeValues': [
                                      {'value': 1, 'attribute': {'id': 'spyJiurH5ax', 'name': 'state'}}
                                  ],
                                  'parent': {'id': '00000000000'}}

        ProvinceFactory(uid='12345678901', province_name='MANICA', description='province 1',
                        data_creation=datetime.date(2016, 8, 15))

        province = Province.objects.first()
        province_dict = convert_province_to_dict(province, '00000000000')

        self.assertEqual(province_dict, expected_province_dict)

    def test_should_convert_district_to_json(self):
        expected_district_dict = {'id': '98765432109',
                                  'name': 'MACOMIA',
                                  'shortName': 'MACOMIA',
                                  'openingDate': '2016-08-30',
                                  'description': 'district 1',
                                  'attributeValues': [
                                      {'value': 1, 'attribute': {'id': 'spyJiurH5ax', 'name': 'state'}}
                                  ],
                                  'parent': {'id': '12345678901'}}

        DistrictFactory(uid='98765432109', district_name='MACOMIA', description='district 1',
                        data_creation=datetime.date(2016, 8, 30))

        district = District.objects.first()
        actual_district_dict = convert_district_to_dict(district, '12345678901')

        self.assertEqual(actual_district_dict, expected_district_dict)

    @patch('datetime.date', FakeDate)
    def should_convert_facility_to_json(self):
        expected_facility_dict = {'id': '98765432109',
                                  'name': 'DESCONHECIDO',
                                  'shortName': 'DESCONHECIDO',
                                  'openingDate': '2016-08-25',
                                  'coordinates': "['-17.15', '35.74']",
                                  'attributeValues': [
                                      {'value': 797, 'attribute': {'id': "TnUcnzIcllL", 'name': "code_us"}},
                                      {'value': 'HEALTH POST', 'attribute': {'id': "YssKBQ4E4Mh", 'name': "sorting_us"}},
                                      {'value': 'LEVEL 1', 'attribute': {'id': "A5NJOV9CQyR", 'name': "level_us"}},
                                      {'value': '', 'attribute': {'id': "TzkNvhmYuKo", 'name': "fea_us"}},
                                      {'value': None,
                                       'attribute': {'id': "wPuwpLLX1Gd", 'name': "province_capital_dist"}},
                                      {'value': '356670060320751', 'attribute': {'id': "Sv6JXRJ9wVe", 'name': "device_serial"}},
                                      {'value': '258823197418', 'attribute': {'id': "MKoA22RCFfC", 'name': "sim_number"}},
                                      {'value': '8925801150348700919', 'attribute': {'id': "WlfBODOi2NW", 'name': "sim_serial"}},
                                      {'value': '97', 'attribute': {'id': "CYZM1npI6Uo", 'name': "device_number"}},
                                      {'value': 1, 'attribute': {'id': "spyJiurH5ax", 'name': "state"}},
                                      {'value': None,
                                       'attribute': {'id': "LBPEcehsQnq", 'name': "person_contact_opt"}},
                                      {'value': None, 'attribute': {'id': "OyKR2g4eHOr", 'name': "phone_contact_opt"}},
                                      {'value': None, 'attribute': {'id': "Jf8hMzLNjdO", 'name': "sim_number_opt"}},
                                      {'value': None, 'attribute': {'id': "hZVWv6sIcSR", 'name': "sim_serial_opt"}},
                                      {'value': '74:ba:db:20:a6:44', 'attribute': {'id': "nP1UXtpMXxE", 'name': "mac_number"}},
                                      {'value': '356670060276714', 'attribute': {'id': "hOzWEm3MT0u", 'name': "device_serial_opt"}},
                                  ],
                                  'parent': {'id': '12345678901'}}

        FacilityFactory(uid='98765432109', facility_name='DESCONHECIDO', sim_number='258823197418',
                        sim_serial='8925801150348700919',latitude='-17.15', longitude='35.74',
                        mac_number='74:ba:db:20:a6:44',device_serial_opt='356670060276714',
                        device_serial='356670060320751', device_number='97')

        facility = Facility.objects.first()
        actual_facility_dict = convert_facility_to_dict(facility, '12345678901')

        self.assertEqual(actual_facility_dict, expected_facility_dict)
