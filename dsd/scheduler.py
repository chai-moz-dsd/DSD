import datetime
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
from dsd.services.dhis2_remote_service import post_data_element_values
from dsd.services.dhis2_send_email_service import dhis2_send_email
from dsd.services.sync_cocid_service import set_coc_id
from dsd.services.validate_data_element_values_service import DataElementValuesValidationService

logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL)


def start():
    updated_bes_middleware_cores = None
    try:
        sync_metadata_to_local()
        # updated_bes_middleware_cores = fetch_updated_data_element_values()
        updated_bes_middleware_cores = sync_business_data_to_local()
    except Exception as e:
        logger.error('Sync error: %s!' % e)
        SyncRecord.get_fail_instance().save()
        send_msg_when_error_happened(('Sync error: %s!' % e), ['sjyuan@thoughtworks.com'])

    post_and_validate_data_element(updated_bes_middleware_cores) if updated_bes_middleware_cores else None


def post_and_validate_data_element(updated_bes_middleware_cores):
    reset_cache()
    post_data_element_values(updated_bes_middleware_cores)
    logger.critical('updated_bes_middleware_cores length=%s' % len(updated_bes_middleware_cores))

    set_coc_id()
    DataElementValuesValidationService().validate_values(updated_bes_middleware_cores)


def sync_business_data_to_local():
    last_successfully_sync_start_time = SyncRecord.get_last_successful_sync_start_time()

    sync_start_time = datetime.datetime.now()
    logger.info('sync_business_data_to_local start time === %s' % sync_start_time)
    updated_bes_middleware_cores = bes_middleware_core_service.sync(last_successfully_sync_start_time)
    sender_middleware_core_service.sync(last_successfully_sync_start_time)
    logger.info('sync_business_data_to_local end time = %s' % datetime.datetime.now())
    SyncRecord.get_successful_instance(sync_start_time).save()

    return updated_bes_middleware_cores


def sync_metadata_to_local():
    logger.info('Sync meta data start...')
    province_service.sync()
    district_service.sync()
    facility_service.sync()
    logger.info('Sync meta data end...')


def reset_cache():
    cache.set(ACCESS_TOKEN, None)
    cache.set(REFRESH_TOKEN, None)


def send_msg_when_error_happened(content, receivers):
    dhis2_send_email('Error happens when element data was syn to dhis2.', content, settings.DEFAULT_FROM_EMAIL,
                     receivers)


def test():
    reset_cache()
    sync_business_data_to_local()
    set_coc_id()
    post_and_validate_data_element()
