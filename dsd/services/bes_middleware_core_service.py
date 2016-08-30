import logging

from dsd.models import BesMiddlewareCore
from dsd.models.remote.bes_middleware_core import BesMiddlewareCore as BesMiddlewareCoreRemote
from dsd.util import id_generator

logger = logging.getLogger(__name__)


def sync():
    all_remote_bes_middleware_cores = BesMiddlewareCoreRemote.objects.all()
    all_local_bes_middleware_cores = get_all_from_local(all_remote_bes_middleware_cores)
    all_valid_local_bes_middleware_cores = filter(is_valid, all_local_bes_middleware_cores)

    save_all(all_valid_local_bes_middleware_cores)


def is_valid(bes_middleware_core):
    return True


def get_all_from_local(all_remote_bes_middleware_cores):
    all_local_bes_middleware_cores = []
    for remote_bes_middleware_core in all_remote_bes_middleware_cores:
        remote_bes_middleware_core.__dict__.pop('_state')
        local_bes_middleware_core = BesMiddlewareCore(**remote_bes_middleware_core.__dict__)
        local_bes_middleware_core.uid = id_generator.generate_id()
        all_local_bes_middleware_cores.append(local_bes_middleware_core)

    return all_local_bes_middleware_cores


def save_all(bes_middleware_cores):
    for bes_middleware_core in bes_middleware_cores:
        bes_middleware_core.save()


def should_be_synced(bes_middleware_core, last_sync_date):
    logger.info('bes_middleware_core date = %s' % bes_middleware_core.creation_date)
    logger.info('last_sync_date date = %s' % last_sync_date)
    return bes_middleware_core.creation_date > last_sync_date
