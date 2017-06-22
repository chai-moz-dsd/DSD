import datetime
import logging

from django.conf import settings
from dsd.models import SyncRecord
from dsd.services import bes_middleware_core_service
from dsd.services import district_service
from dsd.services import facility_service
from dsd.services import province_service
from dsd.services import sender_middleware_core_service
from dsd.services.dhis2_remote_service import post_data_element_values
from dsd.services.dhis2_send_email_service import dhis2_send_email
from dsd.services.sync_cocid_service import set_coc_id
from dsd.services.data_value_validation_service import DataElementValuesValidationService

logger = logging.getLogger(__name__)
# logger.setLevel(logging.CRITICAL)


def start():
    updated_bes_middleware_cores = None
    try:
        logger.info('----------------sync_metadata_to_local_start-----------------')
        sync_metadata_to_local()
        logger.info('----------------sync_metadata_to_local_end-----------------')
        # updated_bes_middleware_cores = fetch_updated_data_element_values()
        logger.info('----------------sync_business_data_to_local_start-----------------')
        updated_bes_middleware_cores = sync_business_data_to_local()
        logger.info('----------------sync_business_data_to_local_end-----------------')
        logger.info('updated_bes_middleware_cores count = %s' % len(updated_bes_middleware_cores))
    except Exception as e:
        logger.error('Sync error: %s!' % e)
        SyncRecord.get_fail_instance().save()
        send_msg_when_error_happened(('Sync error: %s!' % e), ['yuewang@thoughtworks.com'])

    logger.info("---------------updated_bes_middleware_cores---------")
    logger.info(updated_bes_middleware_cores)
    post_and_validate_data_element(updated_bes_middleware_cores) if updated_bes_middleware_cores else None


def post_and_validate_data_element(updated_bes_middleware_cores):
    logger.info('-------set_coc_id_start--------')
    set_coc_id()
    logger.info('-------set_coc_id_end--------')
    logger.info('-------post_data_element_values_start--------')
    post_data_element_values(updated_bes_middleware_cores)
    logger.info('-------post_data_element_values_end--------')
    logger.info('-------validate_values_start--------')
    DataElementValuesValidationService().validate_values(updated_bes_middleware_cores)
    logger.info('-------validate_values_end--------')


def sync_business_data_to_local():
    logger.info('----------last_successfully_sync_start_time_start-------')
    last_successfully_sync_start_time = SyncRecord.get_last_successful_sync_start_time()
    logger.info('----------last_successfully_sync_start_time_end-------')
    logger.info('----------last_successfully_sync_start_time-------', last_successfully_sync_start_time)

    sync_start_time = datetime.datetime.now()
    logger.info('-------sync_business_data_to_local start time === %s' % sync_start_time)

    logger.info('----------updated_bes_middleware_cores_start-------')
    updated_bes_middleware_cores = bes_middleware_core_service.sync(last_successfully_sync_start_time)
    logger.info('----------updated_bes_middleware_cores_end-------')

    logger.info('----------sender_middleware_core_service_start-------')
    sender_middleware_core_service.sync(last_successfully_sync_start_time)
    logger.info('----------sender_middleware_core_service_end-------')
    logger.info('sync_business_data_to_local end time ===== %s' % datetime.datetime.now())

    SyncRecord.get_successful_instance(sync_start_time).save()

    return updated_bes_middleware_cores


def sync_metadata_to_local():
    logger.info('Sync meta data start...')
    logger.info('--------province_start------')
    province_service.sync()
    logger.info('--------province_end------')
    logger.info('--------district_start------')
    district_service.sync()
    logger.info('--------district_end------')
    logger.info('--------facility_start------')
    facility_service.sync()
    logger.info('--------facility_end------')
    logger.info('Sync meta data end...')


def send_msg_when_error_happened(content, receivers):
    dhis2_send_email('Error happens when element data was syn to dhis2.', content, settings.DEFAULT_FROM_EMAIL,
                     receivers)


def test():
    sync_business_data_to_local()
    set_coc_id()
    post_and_validate_data_element()
