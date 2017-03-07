import factory

from dsd.models import DistrictPopulation
from dsd.test.factories.district_factory import DistrictFactory


class DistrictPopulationFactory(factory.DjangoModelFactory):
    class Meta:
        model = DistrictPopulation

    population_size = 1000
    year = 2017
    date_created = None
    district = factory.SubFactory(DistrictFactory)