import factory

from dsd.models import CategoryOption
from dsd.util.id_generator import generate_id


class CategoryOptionFactory(factory.DjangoModelFactory):
    class Meta:
        model = CategoryOption

    id = generate_id()
    name = factory.Iterator(['5 anos', '5-14 anos', '15 anos+'])
