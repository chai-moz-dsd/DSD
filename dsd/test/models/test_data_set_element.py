from django.test import TestCase

from dsd.models import DataSetElement
from dsd.test.factories.data_set_element_factory import DataSetElementFactory


class DataSetElementTest(TestCase):
    def test_should_save_data_set_element(self):
        DataSetElementFactory()
        self.assertEqual(DataSetElement.objects.count(), 1)

    def test_should_find_specific_data_set_element(self):
        element = DataSetElementFactory(data_set_id='123')
        elements = DataSetElement.objects.filter()
        self.assertEqual(elements.count(), 1)
        self.assertEqual(elements[0], element)
