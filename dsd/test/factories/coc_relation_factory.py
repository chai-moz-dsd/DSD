import factory

from dsd.models import COCRelation
from dsd.util.id_generator import generate_id


class COCRelationFactory(factory.DjangoModelFactory):
    class Meta:
        model = COCRelation

    name_in_bes = factory.Iterator(['cases_nv_measles', 'cases_rabies'])
    element_id = generate_id()
    cc_id = generate_id()
    name_of_coc = factory.Iterator(['9-23 meses(Não Vacinados), C', 'C'])
    coc_id = generate_id()
