import factory

from dsd.models import Category
from dsd.util.id_generator import generate_id


class CategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Category

    id = generate_id()
    name = factory.Iterator(['Age Range malaria', 'patient statistics'])

    @factory.post_generation
    def category_options(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for category_option in extracted:
                self.category_options.add(category_option)
