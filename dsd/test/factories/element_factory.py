import factory

from dsd.models.element import Element
from dsd.util.id_generator import generate_id


class ElementFactory(factory.DjangoModelFactory):
    class Meta:
        model = Element

    id = generate_id()
    name = factory.Iterator(['province_capital_dist', 'device_serial_opt', 'code_us', 'device_serial', 'sim_serial'])
    short_name = factory.Iterator(
        ['province_capital_dist', 'device_serial_opt', 'code_us', 'device_serial', 'sim_serial'])
    code = name
    aggregation_type = factory.Iterator(['PLUS', 'SUM'])
    domain_type = factory.Iterator(['AGGREGATE', 'NUMBER'])
    value_type = factory.Iterator(['STRING', 'INTEGER'])
