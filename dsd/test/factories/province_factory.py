import factory

from dsd.models.remote.province import Province


class ProvinceFactory(factory.DjangoModelFactory):
    class Meta:
        model = Province

    province_name = factory.Iterator(
        ['NIASSA', 'CABO DELGADO', 'NAMPULA', 'ZAMBEZIA', 'TETE', 'MANICA', 'SOFALA', 'INHAMBANE', 'GAZA',
         'MAPUTO PROVINCIA', 'MAPUTO CIDADE'])
    description = factory.sequence(lambda n: "description:{0}".format(n))
    data_creation = None
    user_creation = 0
    state = 1
