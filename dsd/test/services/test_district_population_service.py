from datetime import datetime

from django.test import TestCase

from dsd.models.district_population import DistrictPopulation
from dsd.services.district_population_service import is_updated, save_district_populations
from dsd.test.factories.district_factory import DistrictFactory
from dsd.test.factories.district_population_factory import DistrictPopulationFactory


class DistrictPopulationServiceTest(TestCase):
    def test_should_be_false_when_remote_district_not_updated(self):
        date_creation = datetime.today().date()
        district = DistrictFactory()
        district_population_remote = DistrictPopulation(population_size=1000,
                                                        year=2017,
                                                        date_created=date_creation,
                                                        district=district)

        DistrictPopulationFactory(population_size=1000,
                                  year=2017,
                                  date_created=date_creation,
                                  district=district)

        self.assertFalse(is_updated(district_population_remote))

    def test_should_be_true_when_remote_district_updated(self):
        date_creation = datetime.today().date()
        district = DistrictFactory()
        district_population_remote = DistrictPopulation(population_size=1000,
                                                        year=2017,
                                                        date_created=date_creation,
                                                        district=district)

        DistrictPopulationFactory(population_size=1000,
                                  year=2018,
                                  date_created=date_creation,
                                  district=district)

        self.assertTrue(is_updated(district_population_remote))

    def test_should_create_population(self):
        district = DistrictFactory()
        filter_result = DistrictPopulation.objects.filter(district=district)
        self.assertEqual(filter_result.count(), 0)

        date_creation = datetime.today().date()
        population = DistrictPopulation(population_size=1000,
                                        year=2200,
                                        date_created=date_creation,
                                        district=district)
        save_district_populations([population])

        filter_result = DistrictPopulation.objects.filter(district=district)
        self.assertEqual(filter_result.count(), 1)

    def test_should_update_population(self):
        district = DistrictFactory()
        date_creation = datetime.today().date()
        population = DistrictPopulation(population_size=1000,
                                        year=2200,
                                        date_created=date_creation,
                                        district=district)
        save_district_populations([population])

        filter_result = DistrictPopulation.objects.filter(district=district)
        self.assertEqual(filter_result.count(), 1)

        population = DistrictPopulation(population_size=1245,
                                        year=1100,
                                        date_created=date_creation,
                                        district=district)

        save_district_populations([population])

        filter_result = DistrictPopulation.objects.filter(district=district)
        self.assertEqual(filter_result.count(), 1)
        self.assertEqual(filter_result[0].population_size, 1245)
        self.assertEqual(filter_result[0].year, 1100)

