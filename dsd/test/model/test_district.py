from django.test import TestCase

from dsd.models import District
from dsd.models import Province
from dsd.test.factories.district_factory import DistrictFactory


class DistrictTest(TestCase):
    def test_should_save_district(self):
        district = DistrictFactory()
        self.assertEqual(District.objects.count(), 1)
        self.assertEqual(Province.objects.count(), 1)

        DistrictFactory(district_name='BALAMA', state=2, province=district.province)
        self.assertEqual(Province.objects.count(), 1)
        self.assertEqual(District.objects.count(), 2)

    def test_should_find_specific_district(self):
        maputo = DistrictFactory(district_name='MAPUTO PROVINCIA')
        niassa = DistrictFactory(district_name='NIASSA', state=3)
        self.assertEqual(Province.objects.count(), 2)

        actual_districts = District.objects.filter(district_name='MAPUTO PROVINCIA')
        self.assertEqual(actual_districts.count(), 1)
        self.assertEqual(actual_districts[0], maputo)

        actual_districts = District.objects.filter(district_name='NIASSA')
        self.assertEqual(actual_districts.count(), 1)
        self.assertEqual(actual_districts[0], niassa)
