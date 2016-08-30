import logging

from dsd.services.sync.sync_facility import sync_facility
from dsd.services.sync.sync_province import sync_province

from dsd.services.sync.sync_district import sync_district

logger = logging.getLogger(__name__)


def sync_data():
    logger.info('Sync start...')
    sync_metadata()
    logger.info('Sync end...')


def sync_metadata():
    sync_province()
    sync_district()
    sync_facility()
