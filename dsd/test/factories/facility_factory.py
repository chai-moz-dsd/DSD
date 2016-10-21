import factory

from dsd.models import Facility
from dsd.test.factories.district_factory import DistrictFactory
from dsd.test.factories.province_factory import ProvinceFactory
from dsd.util.id_generator import generate_id


class FacilityFactory(factory.DjangoModelFactory):
    class Meta:
        model = Facility

    facility_name = factory.Iterator(['CENTRO DE SAUDE DE CHINETE', 'POSTO DE SAUDE DE KATAPUA',
                                      'HOSPITAL DISTRITAL DE MACOMIA', 'DESCONHECIDO','DESCONHECHOO'])
    uid = generate_id()
    latitude = ''
    longitude = ''
    code_us = '797'
    sorting_us = 'HEALTH POST'
    level_us = 'LEVEL 1'
    fea_us = ''
    province_capital_dist = None
    device_serial = ''
    sim_number = None
    sim_serial = None
    device_number = ''
    person_contact_opt = None
    phone_contact_opt = None
    sim_number_opt = None
    sim_serial_opt = None
    mac_number = ''
    device_serial_opt = ''
    state = 1

    province = factory.SubFactory(ProvinceFactory)
    district = factory.SubFactory(DistrictFactory, province=factory.SelfAttribute('..province'))
