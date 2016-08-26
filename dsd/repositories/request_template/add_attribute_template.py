from dsd.repositories.request_template.dict_template import DictTemplate


class AddAttributeRequestTemplate(DictTemplate):
    payload = {
        'code': '${code}',
        'valueType': '${valueType}',
        'organisationUnitAttribute': '${organisationUnitAttribute}',
        'name': '${name}'
    }
