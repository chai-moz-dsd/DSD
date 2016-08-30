from django.test import TestCase

from dsd.repositories.request_template.add_attribute_template import AddAttributeRequestTemplate
from dsd.util.id_generator import generate_id


class AddAttributeRequestTemplateTest(TestCase):
    template = AddAttributeRequestTemplate()

    def test_should_build_simple_template(self):
        self.template.payload = {
            'id': '${id}',
            'code': '${code}',
            'valueType': '${value_type}',
            'name': '${name}',
            'shortName': '${short_name}',
            'domainType': '${domain_type}',
            'categoryCombo': {'id': '${category_combo}'}
        }

        id_test = generate_id()
        self.assertDictEqual(
            self.template.build(id=id_test, code='123', value_type='NUMBER', short_name='shortName',
                                name='test', domain_type='domainType', category_combo='categoryCombo'), {
                'id': id_test,
                'code': '123',
                'valueType': 'NUMBER',
                'name': 'test',
                'shortName': 'shortName',
                'domainType': 'domainType',
                'categoryCombo': {'id': 'categoryCombo'}
            })
