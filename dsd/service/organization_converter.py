from dsd.util import id_generator


def convert_province_to_json(province, parent_id):
    return {'id': id_generator.generate_id(),
            'name': province.province_name,
            'shortName': province.province_name,
            'openingDate': str(province.data_creation),
            'description': province.description,
            'userCreation': province.user_creation,
            'state': province.state,
            'parent': {'id': parent_id}}


def convert_district_to_json(district, parent_id):
    return {'id': id_generator.generate_id(),
            'name': district.district_name,
            'shortName': district.district_name,
            'openingDate': str(district.data_creation),
            'description': district.description,
            'userCreation': district.user_creation,
            'state': district.state,
            'parent': {'id': parent_id}}
