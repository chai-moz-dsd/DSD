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
            province_dict["attributeValues"] = MoH.clean_attribute_values(province_dict["attributeValues"])
            moh.append(province_dict)
            self.convert_districts(moh, province)

        return moh

    def convert_districts(self, moh, province):
        for district in province.district_set.all():
            district_dict = convert_district_to_dict(district, province.uid)
            district_dict["attributeValues"] = MoH.clean_attribute_values(district_dict["attributeValues"])
            moh.append(district_dict)
            self.convert_facilities(moh, district)

    @staticmethod
    def convert_facilities(moh, district):
        for facility in district.facility_set.all():
            facility_dict = convert_facility_to_dict(facility, district.uid)
            facility_dict["attributeValues"] = MoH.clean_attribute_values(facility_dict["attributeValues"])
            moh.append(facility_dict)

    @staticmethod
    def compact_dict(org_dict):
        return {k: v for k, v in org_dict.items() if (v is not None and v != "")}

    @staticmethod
    def clean_attribute_values(attribute_values):
        new_attributeValues = []
        for attributeValue in attribute_values:
            value = attributeValue["value"]
            if value is not None and value != "":
                new_attributeValues.append(attributeValue)
        return new_attributeValues
