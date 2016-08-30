from dsd.repositories.request_template.dict_template import DictTemplate


class AddAttributeRequestTemplate(DictTemplate):
    payload = {
        'id' : '${uid}',
        'code': '${code}',
        'valueType': '${valueType}',
        'organisationUnitAttribute': '${orgUnitAttr}',
        'name': '${name}'
    }
