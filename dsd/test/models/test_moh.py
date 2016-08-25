import datetime
import json

from django.test import TestCase
from mock import patch

from dsd.models.moh import MoH
from dsd.test.factories.district_factory import DistrictFactory
from dsd.test.factories.facility_factory import FacilityFactory
from dsd.test.factories.province_factory import ProvinceFactory
from dsd.test.helpers.fake_date import FakeDate


class MoHTest(TestCase):
    def setUp(self):
        with open('dsd/test/data/organization_units.json') as organization_units:
            self.expected_dict = json.loads(organization_units.read())

    @patch('datetime.date', FakeDate)
    @patch('dsd.util.id_generator.generate_id')
    def test_should_get_moh(self, mock_generate_id):
        mock_generate_id.side_effect = ['00000000000', '1111111111', '2222222222', '33333333333', '44444444444',
                                        '55555555555', '6666666666']

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

        moh = MoH()
        actual_dict = moh.get_organization_as_dict()

        print(actual_dict)
        print(self.expected_dict)
        self.assertEqual(actual_dict, self.expected_dict)
