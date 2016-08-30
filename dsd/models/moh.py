import datetime

from dsd.models import Province
from dsd.services.organization_service import convert_province_to_dict, convert_district_to_dict, \
    convert_facility_to_dict

MOH_UID = 'MOH12345678'


class MoH(object):
    def __init__(self):
        self.provinces = Province.objects.all()

    def get_organization_as_list(self):
        return self.convert_moh()

    def convert_moh(self):
        moh = [{'id': MOH_UID,
                'name': 'MoH',
                'shortName': 'MoH',
                'openingDate': str(datetime.date.today())
                }]

        return self.convert_provinces(moh, MOH_UID)

    def convert_provinces(self, moh, moh_uid):
        for province in self.provinces:
            province_dict = convert_province_to_dict(province, moh_uid)
            res = MoH.compact_dict(province_dict)
            moh.append(res)
            self.convert_districts(moh, province)

        return moh

    def convert_districts(self, moh, province):
        for district in province.district_set.all():
            district_dict = convert_district_to_dict(district, province.uid)
            res = MoH.compact_dict(district_dict)
            moh.append(res)
            self.convert_facilities(moh, district)

    @staticmethod
    def convert_facilities(moh, district):
        for facility in district.facility_set.all():
            facility_dict = convert_facility_to_dict(facility, district.uid)
            res = MoH.compact_dict(facility_dict)
            moh.append(res)

    @staticmethod
    def compact_dict(org_dict):
        return {k: v for k, v in org_dict.items() if (v is not None and v != "")}
