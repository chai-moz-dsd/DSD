import datetime

from dsd.models import Province
from dsd.service.organization_converter import convert_province_to_json, convert_district_to_json, \
    convert_facility_to_json
from dsd.util import id_generator


class MoH(object):
    def __init__(self):
        self.provinces = Province.objects.all()

    def get_organization_as_dict(self):
        return self.convert()

    def convert(self):
        moh_id = id_generator.generate_id()
        moh = [{'id': moh_id,
                'name': 'MoH',
                'shortName': 'MoH',
                'openingDate': str(datetime.date.today())
                }]
        for province in self.provinces:
            province_id, province_dict = convert_province_to_json(province, moh_id)
            moh.append(province_dict)
            for district in province.district_set.all():
                district_id, district_dict = convert_district_to_json(district, province_id)
                moh.append(district_dict)
                for facility in district.facility_set.all():
                    moh.append(convert_facility_to_json(facility, district_id))

        return moh
