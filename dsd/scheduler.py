import logging

from django.conf import settings
from django.core.cache import cache

from dsd.models import SyncRecord
from dsd.repositories.dhis2_oauth_token import REFRESH_TOKEN, ACCESS_TOKEN
from dsd.services import bes_middleware_core_service
from dsd.services import district_service
from dsd.services import facility_service
from dsd.services import province_service
from dsd.services import sender_middleware_core_service
from dsd.services.bes_middleware_core_service import fetch_updated_data_element_values
from dsd.services.dhis2_remote_service import post_data_element_values
from dsd.services.dhis2_send_email_service import dhis2_send_email
from dsd.services.sync_cocid_service import set_coc_id
from dsd.services.validate_data_element_values_service import DataElementValuesValidationService

logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL)


def start():
    try:
        sync_remote_data_to_local()
        post_and_validate_data_element()
    except Exception as e:
        logger.error('Sync error: %s!' % e)
        SyncRecord.get_fail_instance().save()
        send_msg_when_error_happened(('Sync error: %s!' % e), ['sjyuan@thoughtworks.com'])


def post_and_validate_data_element():
    reset_cache()
    data_element_values = fetch_updated_data_element_values()
    post_data_element_values(data_element_values)
    logger.critical('data_element_values length=%s' % len(data_element_values))

    set_coc_id()
    DataElementValuesValidationService().validate_values(data_element_values)


def sync_remote_data_to_local():
    logger.info('Sync start...')
    last_successfully_sync_time = SyncRecord.get_last_successful_sync_time()
    sync_metadata_to_local()
    sync_data_to_local(last_successfully_sync_time)
    logger.info('Sync success!')
    SyncRecord.get_successful_instance().save()


def sync_metadata_to_local():
    logger.info('Sync meta data start...')
    province_service.sync()
    district_service.sync()
    facility_service.sync()
    logger.info('Sync meta data end...')


def reset_cache():
    cache.set(ACCESS_TOKEN, None)
    cache.set(REFRESH_TOKEN, None)


def sync_data_to_local(last_successfully_sync_time):
    logger.info('Sync data start...')
    bes_middleware_core_service.sync(last_successfully_sync_time)
    sender_middleware_core_service.sync(last_successfully_sync_time)
    logger.info('Sync data end...')


def send_msg_when_error_happened(content, receivers):
    dhis2_send_email('Error happens when element data was syn to dhis2.', content, settings.DEFAULT_FROM_EMAIL,
                     receivers)
