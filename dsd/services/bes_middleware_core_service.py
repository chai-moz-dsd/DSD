import logging

from dsd.models import BesMiddlewareCore, Facility
from dsd.models.remote.bes_middleware_core import BesMiddlewareCore as BesMiddlewareCoreRemote

logger = logging.getLogger(__name__)


def sync(last_successfully_sync_start_time):
    # if not last_successfully_sync_start_time:
    #     all_remote_bes_middleware_cores = BesMiddlewareCoreRemote.objects\
    #         .all().order_by('bes_year', 'bes_number', 'submission_date')
    #     logger.info('=== sync %s items ===' % len(all_remote_bes_middleware_cores))
    #     logger.info('sync all bes_middleware_cores at %s' % last_successfully_sync_start_time)
    # else:
    logger.info('--------all_remote_bes_middleware_cores_start-------')
    all_remote_bes_middleware_cores = BesMiddlewareCoreRemote.objects\
        .filter(middleware_updated_date__gte=last_successfully_sync_start_time)\
        .order_by('bes_year', 'bes_number', 'submission_date')
    logger.info('--------all_remote_bes_middleware_cores_end-------')
    logger.info('--------all_remote_bes_middleware_cores-------', all_remote_bes_middleware_cores)
    logger.info('sync bes_middleware_cores from %s' % last_successfully_sync_start_time)

    logger.info('--------all_translated_bes_middleware_cores_start-------')
    all_translated_bes_middleware_cores = translate_remote_bes_middleware_cores(all_remote_bes_middleware_cores)
    logger.info('--------all_translated_bes_middleware_cores_end-------')
    logger.info('--------all_translated_bes_middleware_cores-------', all_translated_bes_middleware_cores)

    logger.info('--------all_translated_bes_middleware_cores_start-------')
    all_valid_local_bes_middleware_cores = filter(is_valid, all_translated_bes_middleware_cores)
    logger.info('--------all_translated_bes_middleware_cores_end-------')
    logger.info('--------all_valid_local_bes_middleware_cores-------', all_valid_local_bes_middleware_cores)

    bes_middleware_cores = []
    for bes_middleware_core in all_valid_local_bes_middleware_cores:
        bes_middleware_cores.append(save(bes_middleware_core))

    return bes_middleware_cores


def is_valid(bes_middleware_core):
    return True


def translate_remote_bes_middleware_cores(all_remote_bes_middleware_cores):
    all_local_bes_middleware_cores = []
    for remote_bes_middleware_core in all_remote_bes_middleware_cores:
        remote_bes_middleware_core.__dict__.pop('_state')
        local_bes_middleware_core = BesMiddlewareCore(**remote_bes_middleware_core.__dict__)
        if is_data_element_belongs_to_facility(local_bes_middleware_core):
            all_local_bes_middleware_cores.append(local_bes_middleware_core)

    return all_local_bes_middleware_cores


def save(bes_middleware_core):
    result_filter = BesMiddlewareCore.objects.filter(uri=bes_middleware_core.uri)
    if result_filter.count():
        existed_bes_middleware_core = result_filter.first()
        bes_middleware_core.uri = existed_bes_middleware_core.uri
    bes_middleware_core.save()
    return bes_middleware_core


def should_be_synced(bes_middleware_core, last_sync_success_date):
    return bes_middleware_core.middleware_updated_date > last_sync_success_date


def fetch_updated_data_element_values():
    data_element_values = []

    for value in BesMiddlewareCore.objects.all().order_by('bes_year', 'bes_number', 'submission_date'):
        if is_data_element_belongs_to_facility(value):
            data_element_values.append(value)

    return data_element_values


def is_data_element_belongs_to_facility(date_element_value):
    return bool(Facility.objects.filter(id=date_element_value.middleware_facility_id).count())
