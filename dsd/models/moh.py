import datetime

from dsd.models import Province
from dsd.service.organization_converter import convert_province_to_json
from dsd.util import id_generator


class MoH(object):
    def __init__(self):
        self.moh_id = -1
        self.province_id = -1
        self.district_id = -1

    def get_organization_as_json(self):
        return self.get_moh() + self.get_provinces() + self.get_districts() + self.get_facilities()

    def get_moh(self):
        self.moh_id = id_generator.generate_id()

        return [{'id': self.moh_id,
                 'name': 'MoH',
                 'shortName': 'MoH',
                 'openingDate': str(datetime.date.today())
                 }]

    def get_provinces(self):
        provinces = Province.objects.all()
        return [convert_province_to_json(province, self.moh_id) for province in provinces]

    @staticmethod
    def get_districts():
        return []

    @staticmethod
    def get_facilities():
        return []
