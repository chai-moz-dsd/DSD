import factory

from dsd.models import Facility
from dsd.test.factories.district_factory import DistrictFactory
from dsd.test.factories.province_factory import ProvinceFactory


class FacilityFactory(factory.DjangoModelFactory):
    class Meta:
        model = Facility

    facility_name = factory.Iterator(['CENTRO DE SAUDE DE CHINETE', 'POSTO DE SAUDE DE KATAPUA',
                                      'HOSPITAL DISTRITAL DE MACOMIA', 'DESCONHECIDO'])
    latitude = ''
    longitude = ''
    code_us = ''
    sorting_us = ''
    level_us = ''
    fea_us = ''
    province_capital_dist = None
    device_serial = ''
    sim_number = factory.sequence(lambda n: "SimNumber:{0}".format(n))
    sim_serial = factory.sequence(lambda n: "SimSerial:{0}".format(n))
    device_number = ''
    person_contact_opt = ''
    phone_contact_opt = ''
    sim_number_opt = factory.sequence(lambda n: "SimNumberOpt:{0}".format(n))
    sim_serial_opt = factory.sequence(lambda n: "SimSerialOpt:{0}".format(n))
    mac_number = ''
    device_serial_opt = ''
    state = 1

    province = factory.SubFactory(ProvinceFactory)
    district = factory.SubFactory(DistrictFactory, province=factory.SelfAttribute('..province'))
