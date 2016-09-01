from dsd.repositories.request_template.dict_template import DictTemplate


class AddElementRequestTemplate(DictTemplate):
    payload = {
        'id': '${id}',
        'code': '${code}',
        'valueType': '${value_type}',
        'name': '${name}',
        'shortName': '${short_name}',
        'domainType': '${domain_type}',
        'aggregationType': '${aggregation_type}',
        'categoryCombo': {'id': '${category_combo}'}
    }
