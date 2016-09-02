from django.test import TestCase

from dsd.models import CategoryCombination
from dsd.test.factories.category_combination_factory import CategoryCombinationFactory

from dsd.test.factories.category_factory import CategoryFactory
from dsd.test.factories.category_option_factory import CategoryOptionFactory
from dsd.util.id_generator import generate_id


class CategoryCombinationTest(TestCase):
    def test_should_save_category_combination(self):
        CategoryCombinationFactory(id=generate_id())
        self.assertEqual(CategoryCombination.objects.count(), 1)

        CategoryCombinationFactory(id=generate_id())
        self.assertEqual(CategoryCombination.objects.count(), 2)

    def test_should_find_specific_category_combination(self):
        anos5 = CategoryOptionFactory(id=generate_id(), name='5 anos')
        anos5_14 = CategoryOptionFactory(id=generate_id(), name='5-14 anos')
        casos = CategoryOptionFactory(id=generate_id(), name='C')

        range_malaria_name = 'Age Range malaria'
        patient_statistics_name = 'patient statistics'

        range_malaria = CategoryFactory.create(id=generate_id(), name=range_malaria_name,
                                               category_options=(anos5, anos5_14))
        patient_statistics = CategoryFactory(id=generate_id(), name=patient_statistics_name,
                                             category_options=(casos,))

        diarreia_stat_name = 'diarreia stat'
        meningte_stat_name = 'meningte stat'
        diarreia_stat = CategoryCombinationFactory(id=generate_id(), name=diarreia_stat_name,
                                                   categories=(range_malaria, patient_statistics))
        meningte_stat = CategoryCombinationFactory(id=generate_id(), name=meningte_stat_name,
                                                   categories=(patient_statistics,))

        actual_category_combinations = CategoryCombination.objects.filter(name=diarreia_stat_name)
        self.assertEqual(actual_category_combinations.count(), 1)
        self.assertEqual(actual_category_combinations.first(), diarreia_stat)
        self.assertEqual(len(actual_category_combinations.first().categories.all()), 2)

        actual_category_combinations = CategoryCombination.objects.filter(name=meningte_stat_name)
        self.assertEqual(actual_category_combinations.count(), 1)
        self.assertEqual(actual_category_combinations.first(), meningte_stat)
        self.assertEqual(len(actual_category_combinations.first().categories.all()), 1)
