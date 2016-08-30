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
    def test_should_get_moh(self):

        province_1 = ProvinceFactory(uid='11111111111', province_name='NAMPULA', description='province 1',
                                     state=0, data_creation=datetime.date(2016, 8, 25))
        province_2 = ProvinceFactory(uid='22222222222', province_name='TETE', description='province 2', state=1,
                                     data_creation=datetime.date(2016, 8, 25))

        district_1 = DistrictFactory(uid='33333333333', district_name='MACOMIA', description='district 1', state=0,
                                     data_creation=datetime.date(2016, 8, 25), province=province_1)
        district_2 = DistrictFactory(uid='44444444444', district_name='BALAMA', description='district 2', state=1,
                                     data_creation=datetime.date(2016, 8, 25), province=province_2)

        FacilityFactory(uid='55555555555', facility_name='DESCONHECIDO', district=district_1, province=province_1)
        FacilityFactory(uid='66666666666', facility_name='POSTO DE SAUDE', district=district_2, province=province_2)

        moh = MoH()
        actual_dict = moh.get_organization_as_list()

        print(actual_dict)
        self.maxDiff = None
        self.assertEqual(actual_dict, self.expected_dict)
