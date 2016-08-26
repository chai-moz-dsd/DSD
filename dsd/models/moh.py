import datetime

from dsd.models import Province
from dsd.services.organization_service import convert_province_to_dict, convert_district_to_dict, \
    convert_facility_to_dict
from dsd.util import id_generator


class MoH(object):
    def __init__(self):
        self.provinces = Province.objects.all()

    def get_organization_as_dict(self):
        return self.convert_moh()

    def convert_moh(self):
        moh_id = id_generator.generate_id()
        moh = [{'id': moh_id,
                'name': 'MoH',
                'shortName': 'MoH',
                'openingDate': str(datetime.date.today())
                }]

        return self.convert_provinces(moh, moh_id)

    def convert_provinces(self, moh, moh_id):
        for province in self.provinces:
            province_id, province_dict = convert_province_to_dict(province, moh_id)
            moh.append(province_dict)
            self.convert_districts(moh, province, province_id)

        return moh

    @staticmethod
    def convert_districts(moh, province, province_id):
        for district in province.district_set.all():
            district_id, district_dict = convert_district_to_dict(district, province_id)
            moh.append(district_dict)
            MoH.convert_facilities(moh, district, district_id)

    @staticmethod
    def convert_facilities(moh, district, district_id):
        for facility in district.facility_set.all():
            moh.append(convert_facility_to_dict(facility, district_id))
