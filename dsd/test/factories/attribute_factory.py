import factory

from dsd.models import Attribute
from dsd.util.id_generator import generate_id


class AttributeFactory(factory.DjangoModelFactory):
    class Meta:
        model = Attribute

    uid = generate_id()
    name = factory.Iterator(['device_serial_opt', 'code_us', 'device_serial', 'sim_serial'])
    code = name
    value_type = factory.Iterator(['TEXT', 'NUMBER'])
    attr_type = "organisationUnit"