from django.test import TestCase

from dsd.models import Attribute
from dsd.test.factories.attribute_factory import AttributeFactory


class AttributeTest(TestCase):
    def test_should_save_attribute(self):
        AttributeFactory()
        self.assertEqual(Attribute.objects.count(), 1)
        AttributeFactory()
        self.assertEqual(Attribute.objects.count(), 2)

    def test_should_find_specific_attribute(self):
        AttributeFactory(name='sim_serial_opt')
        AttributeFactory(name='device_serial_opt')
        self.assertEqual(Attribute.objects.count(), 2)

        actual_attributes = Attribute.objects.filter(name='sim_serial_opt')
        self.assertEqual(actual_attributes.count(), 1)

        actual_attributes = Attribute.objects.filter(name='null')
        self.assertEqual(actual_attributes.count(), 0)
