from django.test import TestCase

from dsd.repositories.request_template.add_attribute_template import AddAttributeRequestTemplate


class AddAttributeRequestTemplateTest(TestCase):
    template = AddAttributeRequestTemplate()

    def test_should_build_simple_template(self):
        self.template.payload = {
            'code': '${code}',
            'valueType': '${valueType}',
            'organisationUnitAttribute': '${organisationUnitAttribute}',
            'name': '${name}'
        }

        self.assertDictEqual(
            self.template.build(code='123', valueType='NUMBER', organisationUnitAttribute='attribute', name='test'), {
                'code': '123',
                'valueType': 'NUMBER',
                'organisationUnitAttribute': 'attribute',
                'name': 'test'
            })
