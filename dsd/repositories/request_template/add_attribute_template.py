from dsd.repositories.request_template.dict_template import DictTemplate


class AddAttributeRequestTemplate(DictTemplate):
    payload = {
        'id': '${uid}',
        'code': '${code}',
        'valueType': '${value_type}',
        'organisationUnitAttribute': '${org_unit_attr}',
        'name': '${name}'
    }
