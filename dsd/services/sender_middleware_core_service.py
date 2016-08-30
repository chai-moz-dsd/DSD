import logging

from dsd.models import SenderMiddlewareCore
from dsd.models.remote.sender_middleware_core import SenderMiddlewareCore as SenderMiddlewareCoreRemote
from dsd.util import id_generator

logger = logging.getLogger(__name__)


def sync():
    all_remote_sender_middleware_cores = SenderMiddlewareCoreRemote.objects.all()
    all_local_sender_middleware_cores = get_all_from_local(all_remote_sender_middleware_cores)
    all_valid_local_sender_middleware_cores = filter(is_valid, all_local_sender_middleware_cores)

    save_all(all_valid_local_sender_middleware_cores)


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


def save_all(sender_middleware_cores):
    for sender_middleware_core in sender_middleware_cores:
        sender_middleware_core.save()


def should_be_synced(sender_middleware_core, last_sync_date):
    return sender_middleware_core.creation_date > last_sync_date
