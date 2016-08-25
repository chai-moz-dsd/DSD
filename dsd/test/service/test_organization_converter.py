from django.test import TestCase
from mock import patch

from dsd.models import Province
from dsd.service.organization_converter import convert_province_to_json
from dsd.test.factories.province_factory import ProvinceFactory
from dsd.test.helpers.fake_date import FakeDate


class OrganizationConverterTest(TestCase):
    def setUp(self):
        self.expected_province_json = {'id': '12345678901',
                                       'name': 'MANICA',
                                       'shortName': 'MANICA',
                                       'openingDate': '2016-08-25',
                                       'description': 'province 1',
                                       'data_creation': None,
                                       'user_creation': 0,
                                       'state': 1,
                                       'parent': {'id': '00000000000'}}

    @patch('datetime.date', FakeDate)
    @patch('dsd.util.id_generator.generate_id')
    def test_should_convert_province_to_json(self, mock_generate_id):
        mock_generate_id.return_value = '12345678901'
        ProvinceFactory(province_name='MANICA', description='province 1')

        province = Province.objects.first()
        self.assertEqual(convert_province_to_json(province, '00000000000'), self.expected_province_json)
