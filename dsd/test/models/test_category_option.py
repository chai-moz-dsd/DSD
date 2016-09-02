from django.test import TestCase

from dsd.models import CategoryOption
from dsd.test.factories.category_option_factory import CategoryOptionFactory
from dsd.util.id_generator import generate_id


class CategoryOptionTest(TestCase):
    def test_should_save_category_option(self):
        CategoryOptionFactory(id=generate_id())
        self.assertEqual(CategoryOption.objects.count(), 1)

        CategoryOptionFactory(id=generate_id())
        self.assertEqual(CategoryOption.objects.count(), 2)

    def test_should_find_specific_category_option(self):
        anos5 = CategoryOptionFactory(id=generate_id(), name="5 anos")
        anos5_14 = CategoryOptionFactory(id=generate_id(), name="5-14 anos")

        actual_category_options = CategoryOption.objects.filter(name="5 anos")
        self.assertEqual(actual_category_options.count(), 1)
        self.assertEqual(actual_category_options[0], anos5)

        actual_category_options = CategoryOption.objects.filter(name="5-14 anos")
        self.assertEqual(actual_category_options.count(), 1)
        self.assertEqual(actual_category_options[0], anos5_14)

