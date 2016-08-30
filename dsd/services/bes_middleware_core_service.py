import logging

logger = logging.getLogger(__name__)


def should_be_synced(bes_middleware_core, last_sync_date):
    logger.info('bes_middleware_core date = %s' % bes_middleware_core.creation_date)
    logger.info('last_sync_date date = %s' % last_sync_date)
    return bes_middleware_core.creation_date > last_sync_date
