import logging

from dsd.models import Facility
from dsd.models.remote.facility import Facility as FacilityRemote
from dsd.util import id_generator

logger = logging.getLogger(__name__)


def sync():
    all_remote_facilities = FacilityRemote.objects.all()
    all_local_facilities = get_all_local_facilities(all_remote_facilities)
    all_valid_local_facilities = list(filter(is_valid_facility, all_local_facilities))

    save_facilities(all_valid_local_facilities)


def is_valid_facility(facility):
    if not facility.facility_name:
        return False
    if not facility.device_serial:
        return False
    return True


def get_all_local_facilities(all_remote_facilities):
    all_local_facilities = []
    for remote_facility in all_remote_facilities:
        remote_facility.__dict__.pop('_state')
        local_facility = Facility(**remote_facility.__dict__)
        local_facility.uid = id_generator.generate_md5_id(local_facility.facility_name)
        all_local_facilities.append(local_facility)

    return all_local_facilities


def save_facilities(facilities):
    for facility in facilities:
        filter_result = Facility.objects.filter(id=facility.id)
        if not filter_result.count():
            facility.save()
            continue

        if is_updated(facility):
            existing_facility = Facility.objects.get(id=facility.id)
            facility.id = existing_facility.id
            facility.province = existing_facility.province
            facility.district = existing_facility.district
            facility.uid = existing_facility.uid
            facility.save()


def is_updated(facility_remote):
    facility = Facility.objects.get(id=facility_remote.id)
    return facility_remote.facility_name != facility.facility_name or \
           facility_remote.latitude != facility.latitude or \
           facility_remote.longitude != facility.longitude or \
           facility_remote.code_us != facility.code_us or \
           facility_remote.sorting_us != facility.sorting_us or \
           facility_remote.level_us != facility.level_us or \
           facility_remote.fea_us != facility.fea_us or \
           facility_remote.device_serial != facility.device_serial or \
           facility_remote.sim_number != facility.sim_number or \
           facility_remote.sim_serial != facility.sim_serial or \
           facility_remote.device_number != facility.device_number or \
           facility_remote.state != facility.state or \
           facility_remote.person_contact_opt != facility.person_contact_opt or \
           facility_remote.phone_contact_opt != facility.phone_contact_opt or \
           facility_remote.sim_number_opt != facility.sim_number_opt or \
           facility_remote.sim_serial_opt != facility.sim_serial_opt or \
           facility_remote.mac_number != facility.mac_number or \
           facility_remote.device_serial_opt != facility.device_serial_opt or \
           facility_remote.contact_person != facility.contact_person or \
           facility_remote.phone_contact != facility.phone_contact
