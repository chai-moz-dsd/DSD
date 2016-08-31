import logging

from django.core.exceptions import ObjectDoesNotExist

from dsd.models import Facility
from dsd.models.remote.facility import Facility as FacilityRemote
from dsd.util import id_generator

logger = logging.getLogger(__name__)


def sync(sync_time):
    if not sync_time:
        all_remote_facilities = FacilityRemote.objects.all()
        logger.debug('sync all facilities from %s' % sync_time)
    else:
        all_remote_facilities = FacilityRemote.objects.filter(created__gte=sync_time)
        logger.debug('sync facilities from %s' % sync_time)

    all_local_facilities = get_all_local_facilities(all_remote_facilities)
    all_valid_local_facilities = filter(is_valid_facility, all_local_facilities)

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
        local_facility.uid = id_generator.generate_id()
        all_local_facilities.append(local_facility)

    return all_local_facilities


def save_facilities(facilities):
    for facility in facilities:
        try:
            existing_facility = Facility.objects.get(facility_name=facility.facility_name)
            facility.id = existing_facility.id
            facility.uid = existing_facility.uid
        except ObjectDoesNotExist:
            pass
        finally:
            facility.save()
