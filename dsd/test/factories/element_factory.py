import factory

from dsd.models.element import Element
from dsd.test.factories.category_combination_factory import CategoryCombinationFactory
from dsd.util.id_generator import generate_id


class ElementFactory(factory.DjangoModelFactory):
    class Meta:
        model = Element

    id = generate_id()
    name = factory.Iterator(['deaths_diarrhea_04', 'cases_tetanus', 'note_meningitis'])
    short_name = factory.Iterator(['deaths_diarrhea_04', 'cases_tetanus', 'note_meningitis'])
    code = name
    aggregation_type = factory.Iterator(['PLUS', 'SUM'])
    domain_type = factory.Iterator(['AGGREGATE', 'NUMBER'])
    value_type = factory.Iterator(['STRING', 'INTEGER'])
    category_combo = factory.SubFactory(CategoryCombinationFactory)
