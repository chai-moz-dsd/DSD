import datetime

from dsd.util import id_generator


def convert_province_to_json(province, parent_id):
    province_id = id_generator.generate_id()

    return province_id, {'id': province_id,
                         'name': province.province_name,
                         'shortName': province.province_name,
                         'openingDate': str(province.data_creation),
                         'description': province.description,
                         'userCreation': province.user_creation,
                         'state': province.state,
                         'parent': {'id': parent_id}}


def convert_district_to_json(district, parent_id):
    district_id = id_generator.generate_id()

    return district_id, {'id': district_id,
                         'name': district.district_name,
                         'shortName': district.district_name,
                         'openingDate': str(district.data_creation),
                         'description': district.description,
                         'userCreation': district.user_creation,
                         'state': district.state,
                         'parent': {'id': parent_id}}


def convert_facility_to_json(facility, parent_id):
    facility_id = id_generator.generate_id()

    return {'id': facility_id,
            'name': facility.facility_name,
            'shortName': facility.facility_name,
            'openingDate': str(datetime.date.today()),
            'latitude': facility.latitude,
            'longitude': facility.longitude,
            'code_us': facility.code_us,
            'sorting_us': facility.sorting_us,
            'level_us': facility.level_us,
            'fea_us': facility.fea_us,
            'province_capital_dist': facility.province_capital_dist,
            'device_serial': facility.device_serial,
            'sim_number': facility.sim_number,
            'sim_serial': facility.sim_serial,
            'device_number': facility.device_number,
            'state': facility.state,
            'person_contact_opt': facility.person_contact_opt,
            'phone_contact_opt': facility.phone_contact_opt,
            'sim_number_opt': facility.sim_number_opt,
            'sim_serial_opt': facility.sim_serial_opt,
            'mac_number': facility.mac_number,
            'device_serial_opt': facility.device_serial_opt,
            'parent': {'id': parent_id}}
