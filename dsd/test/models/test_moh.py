import datetime
import json

from django.test import TestCase
from mock import patch

from dsd.models.moh import MoH
from dsd.test.factories.province_factory import ProvinceFactory
from dsd.test.helpers.fake_date import FakeDate


class MoHTest(TestCase):
    def setUp(self):
        with open('dsd/test/data/organization_units.json') as organization_units:
            self.expected_json = json.loads(organization_units.read())

    @patch('datetime.date', FakeDate)
    @patch('dsd.util.id_generator.generate_id')
    def test_should_get_moh(self, mock_generate_id):
        mock_generate_id.side_effect = ['00000000000', '12345678901', '98765432109']

        ProvinceFactory(province_name='NAMPULA', description='province 1', state=0, data_creation=datetime.date.today())
        ProvinceFactory(province_name='TETE', description='province 2', state=1, data_creation=datetime.date.today())

        moh = MoH()
        actual_json = moh.get_organization_as_json()
        self.assertEqual(actual_json, self.expected_json)
