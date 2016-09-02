from django.test import TestCase

from dsd.models import Element
from dsd.test.factories.category_combination_factory import CategoryCombinationFactory
from dsd.test.factories.element_factory import ElementFactory
from dsd.util.id_generator import generate_id


class ElementTest(TestCase):
    def test_should_save_element(self):
        ElementFactory(id=generate_id(), category_combo=CategoryCombinationFactory(id=generate_id()))
        self.assertEqual(Element.objects.count(), 1)
        ElementFactory(id=generate_id())
        self.assertEqual(Element.objects.count(), 2)

    def test_should_find_specific_element(self):
        ElementFactory(name='province_capital_dist', id=generate_id(),
                       category_combo=CategoryCombinationFactory(id=generate_id()))
        ElementFactory(name='device_serial_opt', id=generate_id(),
                       category_combo=CategoryCombinationFactory(id=generate_id()))
        self.assertEqual(Element.objects.count(), 2)

        actual_elements = Element.objects.filter(name='province_capital_dist')
        self.assertEqual(actual_elements.count(), 1)

        actual_elements = Element.objects.filter(name='null')
        self.assertEqual(actual_elements.count(), 0)
