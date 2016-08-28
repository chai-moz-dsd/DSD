from django.test import TestCase

from dsd.models.remote.province import Province
from dsd.test.factories.province_factory import ProvinceFactory


class ProvinceTest(TestCase):
    def should_save_province(self):
        ProvinceFactory(province_name='NAMPULA')
        self.assertEqual(Province.objects.count(), 1)

        ProvinceFactory(province_name='NIASSA', state=2)
        self.assertEqual(Province.objects.count(), 2)

    def should_find_specific_province(self):
        maputo = ProvinceFactory(province_name='MAPUTO PROVINCIA')
        niassa = ProvinceFactory(province_name='NIASSA', state=3)

        actual_provinces = Province.objects.filter(province_name='MAPUTO PROVINCIA')
        self.assertEqual(actual_provinces.count(), 1)
        self.assertEqual(actual_provinces[0], maputo)

        actual_provinces = Province.objects.filter(province_name='NIASSA')
        self.assertEqual(actual_provinces.count(), 1)
        self.assertEqual(actual_provinces[0], niassa)
