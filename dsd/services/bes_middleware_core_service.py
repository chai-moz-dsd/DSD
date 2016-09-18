import logging

from dsd.models import BesMiddlewareCore, Facility
from dsd.models.remote.bes_middleware_core import BesMiddlewareCore as BesMiddlewareCoreRemote

logger = logging.getLogger(__name__)


def sync(sync_time):
    if not sync_time:
        all_remote_bes_middleware_cores = BesMiddlewareCoreRemote.objects.all()
        logger.debug('sync all bes_middleware_cores at %s' % sync_time)
    else:
        all_remote_bes_middleware_cores = BesMiddlewareCoreRemote.objects.filter(middleware_updated_date__gte=sync_time)
        logger.debug('sync bes_middleware_cores from %s' % sync_time)

    all_local_bes_middleware_cores = get_all_from_local(all_remote_bes_middleware_cores)
    all_valid_local_bes_middleware_cores = filter(is_valid, all_local_bes_middleware_cores)

    for bes_middleware_core in all_valid_local_bes_middleware_cores:
        save(bes_middleware_core)


def is_valid(bes_middleware_core):
    return True


def get_all_from_local(all_remote_bes_middleware_cores):
    all_local_bes_middleware_cores = []
    for remote_bes_middleware_core in all_remote_bes_middleware_cores:
        remote_bes_middleware_core.__dict__.pop('_state')
        local_bes_middleware_core = BesMiddlewareCore(**remote_bes_middleware_core.__dict__)
        all_local_bes_middleware_cores.append(local_bes_middleware_core)

    return all_local_bes_middleware_cores


def save(bes_middleware_core):
    result_filter = BesMiddlewareCore.objects.filter(uri=bes_middleware_core.uri)
    if result_filter.count():
        existed_bes_middleware_core = result_filter.first()
        bes_middleware_core.uri = existed_bes_middleware_core.uri

    bes_middleware_core.save()


def should_be_synced(bes_middleware_core, last_sync_date):
    return bes_middleware_core.middleware_updated_date > last_sync_date


def fetch_updated_data_element_values():
    data_element_values = []

    for value in BesMiddlewareCore.objects.all():
        if is_data_element_belongs_to_facility(value):
            data_element_values.append(value)

    return data_element_values


def is_data_element_belongs_to_facility(date_element_value):
    return bool(Facility.objects.filter(device_serial=date_element_value.device_id).count())