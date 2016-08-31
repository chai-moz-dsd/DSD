import logging

from dsd.models import SenderMiddlewareCore
from dsd.models.remote.sender_middleware_core import SenderMiddlewareCore as SenderMiddlewareCoreRemote
from dsd.util import id_generator

logger = logging.getLogger(__name__)


def sync(sync_time):
    if not sync_time:
        all_remote_sender_middleware_cores = SenderMiddlewareCoreRemote.objects.all()
        logger.debug('sync all sender_middleware_cores at %s' % sync_time)
    else:
        all_remote_sender_middleware_cores = SenderMiddlewareCoreRemote.objects.filter(last_update_date__gte=sync_time)
        logger.debug('sync sender_middleware_cores from %s' % sync_time)

    all_local_sender_middleware_cores = get_all_from_local(all_remote_sender_middleware_cores)
    all_valid_local_sender_middleware_cores = filter(is_valid, all_local_sender_middleware_cores)

    for sender_middleware_core in all_valid_local_sender_middleware_cores:
        save(sender_middleware_core)


def is_valid(sender_middleware_core):
    return True


def get_all_from_local(all_remote_sender_middleware_cores):
    all_local_sender_middleware_cores = []
    for remote_sender_middleware_core in all_remote_sender_middleware_cores:
        remote_sender_middleware_core.__dict__.pop('_state')
        local_sender_middleware_core = SenderMiddlewareCore(**remote_sender_middleware_core.__dict__)
        local_sender_middleware_core.uid = id_generator.generate_id()
        all_local_sender_middleware_cores.append(local_sender_middleware_core)

    return all_local_sender_middleware_cores


def save(sender_middleware_core):
    result_filter = SenderMiddlewareCore.objects.filter(uri=sender_middleware_core.uri)
    if result_filter.count():
        existed_sender_middleware_core = result_filter.first()
        sender_middleware_core.uri = existed_sender_middleware_core.uri
    sender_middleware_core.save()


def should_be_synced(sender_middleware_core, last_sync_date):
    return sender_middleware_core.last_update_date > last_sync_date
