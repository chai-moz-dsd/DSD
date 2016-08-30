import logging

from dsd.services import bes_middleware_core_service
from dsd.services import district_service
from dsd.services import facility_service
from dsd.services import province_service
from dsd.services import sender_middleware_core_service

logger = logging.getLogger(__name__)


def start():
    logger.info('Sync start...')
    sync_metadata()
    sync_data()
    logger.info('Sync end...')


def sync_metadata():
    province_service.sync()
    district_service.sync()
    facility_service.sync()


def sync_data():
    bes_middleware_core_service.sync()
    sender_middleware_core_service.sync()
