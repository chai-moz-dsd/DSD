from django.test import TestCase
from mock import patch

from dsd.models.moh import MoH
from dsd.test.factories.province_factory import ProvinceFactory
from dsd.test.helpers.fake_date import FakeDate


class MoHTest(TestCase):
    def setUp(self):
        self.expected_json = [{'id': '00000000000',
                               'name': 'MoH',
                               'shortName': 'MoH',
                               'openingDate': '2016-08-25',
                               },
                              {'id': '12345678901',
                               'name': 'NAMPULA',
                               'shortName': 'NAMPULA',
                               'openingDate': '2016-08-25',
                               'description': 'province 1',
                               'data_creation': None,
                               'user_creation': 0,
                               'state': 0,
                               'parent': {'id': '00000000000'}
                               },
                              {'id': '98765432109',
                               'name': 'TETE',
                               'shortName': 'TETE',
                               'openingDate': '2016-08-25',
                               'description': 'province 2',
                               'data_creation': None,
                               'user_creation': 0,
                               'state': 1,
                               'parent': {'id': '00000000000'}
                               }]

    @patch('datetime.date', FakeDate)
    @patch('dsd.util.id_generator.generate_id')
    def test_should_get_moh(self, mock_generate_id):
        mock_generate_id.side_effect = ['00000000000', '12345678901', '98765432109']

        ProvinceFactory(province_name='NAMPULA', description='province 1', state=0)
        ProvinceFactory(province_name='TETE', description='province 2', state=1)

        moh = MoH()
        actual_json = moh.get_organization_as_json()
        self.assertEqual(actual_json, self.expected_json)
