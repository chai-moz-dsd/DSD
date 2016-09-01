def convert_attribute_to_dict(attribute):
    attr_type = attribute.attr_type + "Attribute"
    return {
        'id': attribute.uid,
        'code': attribute.code,
        'valueType': attribute.value_type,
        attr_type: True,
        'name': attribute.name
    }