import datetime

from dsd.util import id_generator


def convert_province_to_json(province, parent_id):
    return {'id': id_generator.generate_id(),
            'name': province.province_name,
            'shortName': province.province_name,
            'openingDate': str(datetime.date.today()),
            'description': province.description,
            'data_creation': province.data_creation,
            'user_creation': province.user_creation,
            'state': province.state,
            'parent': {'id': parent_id}}


def convert_district_to_json(district, parent_id):
    return {'id': id_generator.generate_id(),
            'name': district.district_name,
            'shortName': district.district_name,
            'openingDate': str(datetime.date.today()),
            'description': district.description,
            'data_creation': str(district.data_creation),
            'user_creation': district.user_creation,
            'state': district.state,
            'parent': {'id': parent_id}}
