import factory

from dsd.models import CategoryCombination
from dsd.util.id_generator import generate_id


class CategoryCombinationFactory(factory.DjangoModelFactory):
    class Meta:
        model = CategoryCombination

    id = generate_id()
    name = factory.Iterator(['diarreia stat', 'meningte stat'])

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for category in extracted:
                self.categories.add(category)
