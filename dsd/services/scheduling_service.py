import logging

from dsd.services.sync_district import sync_district
from dsd.services.sync_facility import sync_facility
from dsd.services.sync_province import sync_province

logger = logging.getLogger(__name__)


def sync_data():
    logger.info('Sync start...')
    sync_metadata()
    logger.info('Sync end...')


def sync_metadata():
    sync_province()
    sync_district()
    sync_facility()
