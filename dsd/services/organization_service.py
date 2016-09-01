import datetime


def convert_province_to_dict(province, parent_id):
    return {'id': province.uid,
            'name': province.province_name,
            'shortName': province.province_name,
            'openingDate': str(province.data_creation) if province.data_creation else str(datetime.date.today()),
            'description': province.description,
            'attributeValues': [
                {'value': province.state, 'attribute': {'id': "spyJiurH5ax", 'name': "state"}}
            ],
            'parent': {'id': parent_id}}


def convert_district_to_dict(district, parent_id):
    return {'id': district.uid,
            'name': district.district_name,
            'shortName': district.district_name,
            'openingDate': str(district.data_creation) if district.data_creation else str(datetime.date.today()),
            'description': district.description,
            'attributeValues': [
                {'value': district.state, 'attribute': {'id': "spyJiurH5ax", 'name': "state"}}
            ],
            'parent': {'id': parent_id}}


def convert_facility_to_dict(facility, parent_id):
    facility_dict = {'id': facility.uid,
                     'name': facility.facility_name,
                     'shortName': facility.facility_name,
                     'openingDate': str(datetime.date.today()),
                     'attributeValues': [
                         {'value': facility.code_us, 'attribute': {'id': "TnUcnzIcllL", 'name': "code_us"}},
                         {'value': facility.sorting_us, 'attribute': {'id': "YssKBQ4E4Mh", 'name': "sorting_us"}},
                         {'value': facility.level_us, 'attribute': {'id': "A5NJOV9CQyR", 'name': "level_us"}},
                         {'value': facility.fea_us, 'attribute': {'id': "TzkNvhmYuKo", 'name': "fea_us"}},
                         {'value': facility.province_capital_dist,
                          'attribute': {'id': "wPuwpLLX1Gd", 'name': "province_capital_dist"}},
                         {'value': facility.device_serial, 'attribute': {'id': "Sv6JXRJ9wVe", 'name': "device_serial"}},
                         {'value': facility.sim_number, 'attribute': {'id': "MKoA22RCFfC", 'name': "sim_number"}},
                         {'value': facility.sim_serial, 'attribute': {'id': "WlfBODOi2NW", 'name': "sim_serial"}},
                         {'value': facility.device_number, 'attribute': {'id': "CYZM1npI6Uo", 'name': "device_number"}},
                         {'value': facility.state, 'attribute': {'id': "spyJiurH5ax", 'name': "state"}},
                         {'value': facility.person_contact_opt,
                          'attribute': {'id': "LBPEcehsQnq", 'name': "person_contact_opt"}},
                         {'value': facility.phone_contact_opt,
                          'attribute': {'id': "OyKR2g4eHOr", 'name': "phone_contact_opt"}},
                         {'value': facility.sim_number_opt,
                          'attribute': {'id': "Jf8hMzLNjdO", 'name': "sim_number_opt"}},
                         {'value': facility.sim_serial_opt,
                          'attribute': {'id': "hZVWv6sIcSR", 'name': "sim_serial_opt"}},
                         {'value': facility.mac_number, 'attribute': {'id': "nP1UXtpMXxE", 'name': "mac_number"}},
                         {'value': facility.device_serial_opt,
                          'attribute': {'id': "hOzWEm3MT0u", 'name': "device_serial_opt"}},
                     ],
                     'parent': {'id': parent_id}}
    if (facility.latitude and facility.longitude):
        facility_dict['coordinates'] =  "[\"%s\", \"%s\"]" % (facility.latitude, facility.longitude)
    return facility_dict