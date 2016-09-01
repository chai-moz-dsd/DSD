import logging

from dsd.models import SyncRecord
from dsd.services import bes_middleware_core_service
from dsd.services import dhis2_remote_service
from dsd.services import district_service
from dsd.services import facility_service
from dsd.services import province_service
from dsd.services import sender_middleware_core_service

logger = logging.getLogger(__name__)


def start():
    try:
        logger.info('Sync start...')
        sync_time = SyncRecord.get_last_successful_sync_time()

        sync_metadata()
        sync_data(sync_time)

        dhis2_remote_service.post_attributes()
        dhis2_remote_service.post_organization_units()
        dhis2_remote_service.post_elements()
        dhis2_remote_service.post_data_set()

        logger.info('Sync success!')
        SyncRecord.get_successful_instance().save()
    except Exception as e:
        logger.error('Sync error: %s!' % e)
        SyncRecord.get_fail_instance().save()


def sync_metadata():
    province_service.sync()
    district_service.sync()
    facility_service.sync()


def sync_data(sync_time):
    bes_middleware_core_service.sync(sync_time)
    sender_middleware_core_service.sync(sync_time)
