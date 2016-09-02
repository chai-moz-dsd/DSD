from django.test import TestCase

from dsd.models import Category
from dsd.test.factories.category_factory import CategoryFactory

from dsd.test.factories.category_option_factory import CategoryOptionFactory
from dsd.util.id_generator import generate_id


class CategoryTest(TestCase):
    def test_should_save_category_option(self):
        CategoryFactory(id=generate_id())
        self.assertEqual(Category.objects.count(), 1)

        CategoryFactory(id=generate_id())
        self.assertEqual(Category.objects.count(), 2)

    def test_should_find_specific_category_option(self):
        anos5 = CategoryOptionFactory(id=generate_id(), name="5 anos")
        anos5_14 = CategoryOptionFactory(id=generate_id(), name="5-14 anos")
        casos = CategoryOptionFactory(id=generate_id(), name="C")

        range_malaria_name = "Age Range malaria"
        patient_statistics_name = "patient statistics"

        range_malaria = CategoryFactory(id=generate_id(), name=range_malaria_name, category_options=(anos5, anos5_14))
        patient_statistics = CategoryFactory(id=generate_id(), name=patient_statistics_name, category_options=(casos,))

        actual_category = Category.objects.filter(name=range_malaria_name)
        self.assertEqual(actual_category.count(), 1)
        self.assertEqual(actual_category.first(), range_malaria)
        self.assertEqual(len(actual_category.first().category_options.all()), 2)

        actual_category = Category.objects.filter(name=patient_statistics_name)
        self.assertEqual(actual_category.count(), 1)
        self.assertEqual(actual_category.first(), patient_statistics)
        self.assertEqual(len(actual_category.first().category_options.all()), 1)
