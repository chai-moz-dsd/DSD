from unittest import TestCase

from dsd.util import id_generator


class IdGeneratorTest(TestCase):
    def test_should_generate_11_bit_id(self):
        self.assertEqual(len(id_generator.generate_id()), 11)

    def test_should_generate_11_bit_md5_id_by_name(self):
        self.assertEqual(len(id_generator.generate_md5_id('chai')), 11)

    def test_should_generate_the_same_11_bit_md5_ids_by_same_names(self):
        name = 'chai'
        self.assertEqual(id_generator.generate_md5_id(name), id_generator.generate_md5_id(name))
