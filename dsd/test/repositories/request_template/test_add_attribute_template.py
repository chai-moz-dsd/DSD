from django.test import TestCase

from dsd.repositories.request_template.add_attribute_template import AddAttributeRequestTemplate


class AddAttributeRequestTemplateTest(TestCase):
    template = AddAttributeRequestTemplate()

    def test_should_build_simple_template(self):
        self.template.payload = {
            'code': '${code}',
            'valueType': '${value_type}',
            'organisationUnitAttribute': '${org_unit_attr}',
            'name': '${name}'
        }

        self.assertDictEqual(
            self.template.build(code='123', value_type='NUMBER', org_unit_attr='attribute', name='test'), {
                'code': '123',
                'valueType': 'NUMBER',
                'organisationUnitAttribute': 'attribute',
                'name': 'test'
            })
