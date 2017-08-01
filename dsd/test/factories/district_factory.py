import factory

from dsd.models import District
from dsd.test.factories.province_factory import ProvinceFactory


class DistrictFactory(factory.DjangoModelFactory):
    class Meta:
        model = District

    id = factory.Iterator([6446, 7447, 8480, 9555])
    district_name = factory.Iterator(['ANCUABE', 'BALAMA', 'CHIURE', 'CIADADE DE PEMBA', 'IBO', 'MACOMIA'])
    description = factory.sequence(lambda n: "Description:{0}".format(n))
    user_creation = 0
    data_creation = None
    state = 1
    province = factory.SubFactory(ProvinceFactory)
