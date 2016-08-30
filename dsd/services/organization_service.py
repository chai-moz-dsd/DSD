import datetime


def convert_province_to_dict(province, parent_id):
    return {'id': province.uid,
            'name': province.province_name,
            'shortName': province.province_name,
            'openingDate': str(province.data_creation) if province.data_creation else str(datetime.date.today()),
            'description': province.description,
            'userCreation': province.user_creation,
            'state': province.state,
            'parent': {'id': parent_id}}


def convert_district_to_dict(district, parent_id):
    return {'id': district.uid,
            'name': district.district_name,
            'shortName': district.district_name,
            'openingDate': str(district.data_creation) if district.data_creation else str(datetime.date.today()),
            'description': district.description,
            'userCreation': district.user_creation,
            'state': district.state,
            'parent': {'id': parent_id}}


def convert_facility_to_dict(facility, parent_id):
    return {'id': facility.uid,
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
