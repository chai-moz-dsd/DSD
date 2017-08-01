import logging

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from dsd.models.remote.facility import Facility as FacilityRemote
from dsd.services.facility_service import is_updated
from dsd.test.factories.facility_factory import FacilityFactory

logger = logging.getLogger(__name__)


class FacilityServiceTest(TestCase):
    def test_should_be_false_when_remote_facility_not_updated(self):
        facility_remote = FacilityRemote(id=9999, facility_name='DESCONHECIDO', latitude='55', longitude='55', code_us='797',
                                         sorting_us='HEALTH POST', level_us='LEVEL 1', fea_us='fea_us',
                                         device_serial='353288063532000',
                                         device_number='353288063532000', person_contact_opt=None,
                                         phone_contact_opt=None, sim_number_opt=None, sim_serial_opt=None,
                                         mac_number='AC-DF-E90-JA-33',
                                         device_serial_opt='', state=1, contact_person='', phone_contact='')
        FacilityFactory(id=9999, facility_name='DESCONHECIDO', latitude='55', longitude='55', code_us='797',
                        sorting_us='HEALTH POST', level_us='LEVEL 1',
                        fea_us='fea_us', device_serial='353288063532000',
                        device_number='353288063532000', person_contact_opt=None, phone_contact_opt=None,
                        sim_number_opt=None, sim_serial_opt=None, mac_number='AC-DF-E90-JA-33',
                        device_serial_opt='', state=1, contact_person='', phone_contact='')
        self.assertFalse(is_updated(facility_remote))

    def test_should_be_false_when_remote_facility_latitude_updated(self):
        facility_remote = FacilityRemote(id=9999, facility_name='DESCONHECIDO', latitude='50', longitude='55', code_us='797',
                                         sorting_us='HEALTH POST',
                                         level_us='LEVEL 1', fea_us='fea_us', 
                                         device_serial='353288063532000',
                                         device_number='353288063532000', person_contact_opt=None,
                                         phone_contact_opt=None, sim_number_opt=None, sim_serial_opt=None,
                                         mac_number='AC-DF-E90-JA-33',
                                         device_serial_opt='', state=1)
        FacilityFactory(id=9999, facility_name='DESCONHECIDO', latitude='55', longitude='55', code_us='797',
                        sorting_us='HEALTH POST', level_us='LEVEL 1',
                        fea_us='fea_us', device_serial='353288063532000',
                        device_number='353288063532000', person_contact_opt=None, phone_contact_opt=None,
                        sim_number_opt=None, sim_serial_opt=None,
                        mac_number='AC-DF-E90-JA-33', device_serial_opt='', state=1)
        self.assertTrue(is_updated(facility_remote))

    def test_should_be_false_when_remote_facility_longitude_updated(self):
        facility_remote = FacilityRemote(id=9999, facility_name='DESCONHECIDO', latitude='55', longitude='50', code_us='797',
                                         sorting_us='HEALTH POST',
                                         level_us='LEVEL 1', fea_us='fea_us', 
                                         device_serial='353288063532000',
                                         device_number='353288063532000', person_contact_opt=None,
                                         phone_contact_opt=None, sim_number_opt=None, sim_serial_opt=None,
                                         mac_number='AC-DF-E90-JA-33',
                                         device_serial_opt='', state=1)
        FacilityFactory(id=9999, facility_name='DESCONHECIDO', latitude='55', longitude='55', code_us='797',
                        sorting_us='HEALTH POST', level_us='LEVEL 1',
                        fea_us='fea_us', device_serial='353288063532000',
                        device_number='353288063532000', person_contact_opt=None, phone_contact_opt=None,
                        sim_number_opt=None, sim_serial_opt=None,
                        mac_number='AC-DF-E90-JA-33', device_serial_opt='', state=1)
        self.assertTrue(is_updated(facility_remote))

    def test_should_be_false_when_remote_facility_code_us_updated(self):
        facility_remote = FacilityRemote(id=9999, facility_name='DESCONHECIDO', latitude='55', longitude='55', code_us='790',
                                         sorting_us='HEALTH POST',
                                         level_us='LEVEL 1', fea_us='fea_us', 
                                         device_serial='353288063532000',
                                         device_number='353288063532000', person_contact_opt=None,
                                         phone_contact_opt=None, sim_number_opt=None, sim_serial_opt=None,
                                         mac_number='AC-DF-E90-JA-33',
                                         device_serial_opt='', state=1)
        FacilityFactory(id=9999, facility_name='DESCONHECIDO', latitude='55', longitude='55', code_us='797',
                        sorting_us='HEALTH POST', level_us='LEVEL 1',
                        fea_us='fea_us', device_serial='353288063532000',
                        device_number='353288063532000', person_contact_opt=None, phone_contact_opt=None,
                        sim_number_opt=None, sim_serial_opt=None,
                        mac_number='AC-DF-E90-JA-33', device_serial_opt='', state=1)
        self.assertTrue(is_updated(facility_remote))

    def test_should_be_false_when_remote_facility_sorting_us_updated(self):
        facility_remote = FacilityRemote(id=9999, facility_name='DESCONHECIDO', latitude='55', longitude='55', code_us='797',
                                         sorting_us='HEALTH POST1',
                                         level_us='LEVEL 1', fea_us='fea_us', 
                                         device_serial='353288063532000',
                                         device_number='353288063532000', person_contact_opt=None,
                                         phone_contact_opt=None, sim_number_opt=None, sim_serial_opt=None,
                                         mac_number='AC-DF-E90-JA-33',
                                         device_serial_opt='', state=1)
        FacilityFactory(id=9999, facility_name='DESCONHECIDO', latitude='55', longitude='55', code_us='797',
                        sorting_us='HEALTH POST', level_us='LEVEL 1',
                        fea_us='fea_us', device_serial='353288063532000',
                        device_number='353288063532000', person_contact_opt=None, phone_contact_opt=None,
                        sim_number_opt=None, sim_serial_opt=None,
                        mac_number='AC-DF-E90-JA-33', device_serial_opt='', state=1)
        self.assertTrue(is_updated(facility_remote))

    def test_should_be_false_when_remote_facility_level_us_updated(self):
        facility_remote = FacilityRemote(id=9999, facility_name='DESCONHECIDO', latitude='55', longitude='55', code_us='797',
                                         sorting_us='HEALTH POST',
                                         level_us='LEVEL 0', fea_us='fea_us', 
                                         device_serial='353288063532000',
                                         device_number='353288063532000', person_contact_opt=None,
                                         phone_contact_opt=None, sim_number_opt=None, sim_serial_opt=None,
                                         mac_number='AC-DF-E90-JA-33',
                                         device_serial_opt='', state=1)
        FacilityFactory(id=9999, facility_name='DESCONHECIDO', latitude='55', longitude='55', code_us='797',
                        sorting_us='HEALTH POST', level_us='LEVEL 1',
                        fea_us='fea_us', device_serial='353288063532000',
                        device_number='353288063532000', person_contact_opt=None, phone_contact_opt=None,
                        sim_number_opt=None, sim_serial_opt=None,
                        mac_number='AC-DF-E90-JA-33', device_serial_opt='', state=1)
        self.assertTrue(is_updated(facility_remote))

    def test_should_be_false_when_remote_fea_us_updated(self):
        facility_remote = FacilityRemote(id=9999, facility_name='DESCONHECIDO', latitude='55', longitude='55', code_us='797',
                                         sorting_us='HEALTH POST',
                                         level_us='LEVEL 1', fea_us='fea_us1', 
                                         device_serial='353288063532000',
                                         device_number='353288063532000', person_contact_opt=None,
                                         phone_contact_opt=None, sim_number_opt=None, sim_serial_opt=None,
                                         mac_number='AC-DF-E90-JA-33',
                                         device_serial_opt='', state=1)
        FacilityFactory(id=9999, facility_name='DESCONHECIDO', latitude='55', longitude='55', code_us='797',
                        sorting_us='HEALTH POST', level_us='LEVEL 1',
                        fea_us='fea_us', device_serial='353288063532000',
                        device_number='353288063532000', person_contact_opt=None, phone_contact_opt=None,
                        sim_number_opt=None, sim_serial_opt=None,
                        mac_number='AC-DF-E90-JA-33', device_serial_opt='', state=1)
        self.assertTrue(is_updated(facility_remote))

    def test_should_be_false_when_remote_facility_device_serial_updated(self):
        facility_remote = FacilityRemote(id=9999, facility_name='DESCONHECIDO', latitude='55', longitude='55', code_us='797',
                                         sorting_us='HEALTH POST',
                                         level_us='LEVEL 1', fea_us='fea_us', 
                                         device_serial='353288063532001',
                                         device_number='353288063532000', person_contact_opt=None,
                                         phone_contact_opt=None, sim_number_opt=None, sim_serial_opt=None,
                                         mac_number='AC-DF-E90-JA-33',
                                         device_serial_opt='', state=1)
        FacilityFactory(id=9999, facility_name='DESCONHECIDO', latitude='55', longitude='55', code_us='797',
                        sorting_us='HEALTH POST', level_us='LEVEL 1',
                        fea_us='fea_us', device_serial='353288063532000',
                        device_number='353288063532000', person_contact_opt=None, phone_contact_opt=None,
                        sim_number_opt=None, sim_serial_opt=None,
                        mac_number='AC-DF-E90-JA-33', device_serial_opt='', state=1)
        self.assertTrue(is_updated(facility_remote))

    def test_should_be_false_when_remote_facility_device_number_updated(self):
        facility_remote = FacilityRemote(id=9999, facility_name='DESCONHECIDO', latitude='55', longitude='55', code_us='797',
                                         sorting_us='HEALTH POST',
                                         level_us='LEVEL 1', fea_us='fea_us', 
                                         device_serial='353288063532000',
                                         device_number='353288063532001', person_contact_opt=None,
                                         phone_contact_opt=None, sim_number_opt=None, sim_serial_opt=None,
                                         mac_number='AC-DF-E90-JA-33',
                                         device_serial_opt='', state=1)
        FacilityFactory(id=9999, facility_name='DESCONHECIDO', latitude='55', longitude='55', code_us='797',
                        sorting_us='HEALTH POST', level_us='LEVEL 1',
                        fea_us='fea_us', device_serial='353288063532000',
                        device_number='353288063532000', person_contact_opt=None, phone_contact_opt=None,
                        sim_number_opt=None, sim_serial_opt=None,
                        mac_number='AC-DF-E90-JA-33', device_serial_opt='', state=1)
        self.assertTrue(is_updated(facility_remote))

    def test_should_be_false_when_remote_facility_mac_number_updated(self):
        facility_remote = FacilityRemote(id=9999, facility_name='DESCONHECIDO', latitude='55', longitude='55', code_us='797',
                                         sorting_us='HEALTH POST',
                                         level_us='LEVEL 1', fea_us='fea_us', 
                                         device_serial='353288063532000',
                                         device_number='353288063532000', person_contact_opt=None,
                                         phone_contact_opt=None, sim_number_opt=None, sim_serial_opt=None,
                                         mac_number='AC-DF-E90-JA-30',
                                         device_serial_opt='', state=1)
        FacilityFactory(id=9999, facility_name='DESCONHECIDO', latitude='55', longitude='55', code_us='797',
                        sorting_us='HEALTH POST', level_us='LEVEL 1',
                        fea_us='fea_us', device_serial='353288063532000',
                        device_number='353288063532000', person_contact_opt=None, phone_contact_opt=None,
                        sim_number_opt=None, sim_serial_opt=None,
                        mac_number='AC-DF-E90-JA-33', device_serial_opt='', state=1)
        self.assertTrue(is_updated(facility_remote))

    def test_should_be_false_when_remote_facility_state_updated(self):
        facility_remote = FacilityRemote(id=9999, facility_name='DESCONHECIDO', latitude='55', longitude='55', code_us='797',
                                         sorting_us='HEALTH POST',
                                         level_us='LEVEL 1', fea_us='fea_us', 
                                         device_serial='353288063532000',
                                         device_number='353288063532000', person_contact_opt=None,
                                         phone_contact_opt=None, sim_number_opt=None, sim_serial_opt=None,
                                         mac_number='AC-DF-E90-JA-33',
                                         device_serial_opt='', state=0)
        FacilityFactory(id=9999, facility_name='DESCONHECIDO', latitude='55', longitude='55', code_us='797',
                        sorting_us='HEALTH POST', level_us='LEVEL 1',
                        fea_us='fea_us', device_serial='353288063532000',
                        device_number='353288063532000', person_contact_opt=None, phone_contact_opt=None,
                        sim_number_opt=None, sim_serial_opt=None,
                        mac_number='AC-DF-E90-JA-33', device_serial_opt='', state=1)
        self.assertTrue(is_updated(facility_remote))

    def test_should_raise_exception_when_remote_facility_name_updated(self):
        facility_remote = FacilityRemote(facility_name='DESCONHECIDO')

        FacilityFactory(facility_name='test')

        with self.assertRaises(ObjectDoesNotExist):
            is_updated(facility_remote)
