import uuid
from datetime import datetime

import factory

from dsd.models import Province


class ProvinceFactory(factory.DjangoModelFactory):
    class Meta:
        model = Province

    id = factory.Iterator([446, 447, 480, 555])
    uid = uuid.uuid4()
    province_name = factory.Iterator(
        ['NIASSA', 'CABO DELGADO', 'NAMPULA', 'ZAMBEZIA', 'TETE', 'MANICA', 'SOFALA', 'INHAMBANE', 'GAZA',
         'MAPUTO PROVINCIA', 'MAPUTO CIDADE'])
    description = factory.sequence(lambda n: "description:{0}".format(n))
    data_creation = datetime.today()
    user_creation = 0
    state = 1
