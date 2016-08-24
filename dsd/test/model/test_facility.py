from django.test import TestCase

from dsd.models import Facility
from dsd.models import Province
from dsd.test.factories.facility_factory import FacilityFactory


class FacilityTest(TestCase):
    def test_should_save_facility(self):
        FacilityFactory()
        self.assertEqual(Facility.objects.count(), 1)
        self.assertEqual(Province.objects.count(), 1)

        FacilityFactory()
        self.assertEqual(Province.objects.count(), 2)
        self.assertEqual(Facility.objects.count(), 2)

    def test_should_find_specific_facility(self):
        hospital = FacilityFactory(facility_name='HOSPITAL DISTRITAL DE MACOMIA')
        des = FacilityFactory(facility_name='DESCONHECIDO', state=3)
        self.assertEqual(Province.objects.count(), 2)

        actual_facilities = Facility.objects.filter(facility_name='HOSPITAL DISTRITAL DE MACOMIA')
        self.assertEqual(actual_facilities.count(), 1)
        self.assertEqual(actual_facilities[0], hospital)

        actual_facilities = Facility.objects.filter(facility_name='DESCONHECIDO')
        self.assertEqual(actual_facilities.count(), 1)
        self.assertEqual(actual_facilities[0], des)
