from unittest import TestCase

from mock import patch
from dsd.deployment.validation_initializer import assemble_left_side_expression
from dsd.services.data_value_validation_service import DataElementValuesValidationService


class ValidationInitializerServiceTest(TestCase):
    @patch.object(DataElementValuesValidationService, 'get_element_ids')
    def test_should_assemble_left_side_expression(self, mock_get_element_ids):
        mock_get_element_ids.return_value = ['a.a', 'b.b', 'c.c']
        result = assemble_left_side_expression('', '')
        self.assertEqual(result, '#{a.a}+#{b.b}+#{c.c}')
