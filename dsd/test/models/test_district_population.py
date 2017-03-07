from django.test import TestCase

from dsd.models import District
from dsd.models import DistrictPopulation
from dsd.test.factories.district_factory import DistrictFactory
from dsd.test.factories.district_population_factory import DistrictPopulationFactory


class DistrictPopulationTest(TestCase):
    def test_should_save_district_population(self):
        DistrictPopulationFactory()
        self.assertEqual(DistrictPopulation.objects.count(), 1)
        self.assertEqual(District.objects.count(), 1)

        district = DistrictFactory()
        DistrictPopulationFactory(population_size=5000, year=2015, district=district)
        self.assertEqual(DistrictPopulation.objects.count(), 2)
        self.assertEqual(District.objects.count(), 2)

    def test_should_find_specific_population_by_district(self):
        mapotu = DistrictFactory(district_name='MAPOTU')
        DistrictPopulationFactory(district=mapotu)
        district_population = DistrictPopulation.objects.filter(district=mapotu)
        self.assertEqual(district_population.count(), 1)
        self.assertEqual(district_population[0].population_size, 1000)

        manach = DistrictFactory(district_name='MANACH')
        DistrictPopulationFactory(district=manach, population_size=5000)
        district_population = DistrictPopulation.objects.filter(district=manach)
        self.assertEqual(district_population.count(), 1)
        self.assertEqual(district_population[0].population_size, 5000)

