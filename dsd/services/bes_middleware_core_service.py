import logging
from datetime import datetime

from dsd.config import dhis2_config
from dsd.models import BesMiddlewareCore
from dsd.models import Element
from dsd.models import Facility
from dsd.models.remote.bes_middleware_core import BesMiddlewareCore as BesMiddlewareCoreRemote

logger = logging.getLogger(__name__)


def sync():
    all_remote_bes_middleware_cores = BesMiddlewareCoreRemote.objects.all()
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
    return bes_middleware_core.last_update_date > last_sync_date


def build_post_data_set_request_body_as_dict(bes_middleware_core):
    elements = Element.objects.all()
    data_values = []
    for element in elements:
        data_values.append({
            'dataElement': element.id,
            'value': getattr(bes_middleware_core, element.name)
        })

    now = datetime.now()
    return {
        "dataSet": dhis2_config.DATA_SET_ID,
        "completeData": str(now),
        "period": str(now.strftime('%Y%m')),
        "orgUnit": Facility.objects.get(device_serial=bes_middleware_core.device_id).uid,
        "dataValues": data_values
    }
