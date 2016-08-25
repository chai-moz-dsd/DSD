import datetime

from django.test import TestCase
from mock import patch

from dsd.models import Province, District
from dsd.service.organization_converter import convert_province_to_json, convert_district_to_json
from dsd.test.factories.province_factory import ProvinceFactory
from dsd.test.factories.district_factory import DistrictFactory
from dsd.test.helpers.fake_date import FakeDate


class OrganizationConverterTest(TestCase):
    @patch('datetime.date', FakeDate)
    @patch('dsd.util.id_generator.generate_id')
    def test_should_convert_province_to_json(self, mock_generate_id):
        expected_province_json = {'id': '12345678901',
                                  'name': 'MANICA',
                                  'shortName': 'MANICA',
                                  'openingDate': '2016-08-25',
                                  'description': 'province 1',
                                  'userCreation': 0,
                                  'state': 1,
                                  'parent': {'id': '00000000000'}}

        mock_generate_id.return_value = '12345678901'
        ProvinceFactory(province_name='MANICA', description='province 1', data_creation=datetime.date.today())

        province = Province.objects.first()
        self.assertEqual(convert_province_to_json(province, '00000000000'), expected_province_json)

    @patch('datetime.date', FakeDate)
    @patch('dsd.util.id_generator.generate_id')
    def test_should_convert_district_to_json(self, mock_generate_id):
        expected_district_json = {'id': '98765432109',
                                  'name': 'MACOMIA',
                                  'shortName': 'MACOMIA',
                                  'openingDate': '2016-08-25',
                                  'description': 'district 1',
                                  'userCreation': 0,
                                  'state': 1,
                                  'parent': {'id': '12345678901'}}

        mock_generate_id.return_value = '98765432109'
        DistrictFactory(district_name='MACOMIA', description='district 1', data_creation=datetime.date.today())

        district = District.objects.first()
        self.assertEqual(convert_district_to_json(district, '12345678901'), expected_district_json)
