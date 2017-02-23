import logging

from dsd.deployment.validation_initializer import post_all_validation_rule_and_group
from dsd.models import SyncRecord
from dsd.scheduler import sync_business_data_to_local, sync_metadata_to_local
from dsd.services.bes_middleware_core_service import fetch_updated_data_element_values
from dsd.services.dhis2_remote_service import post_attributes, post_organization_units, post_category_options, post_categories, post_category_combinations, post_elements, post_data_set, assign_all_org_to_user, set_org_unit_level, post_data_element_values, \
    set_user_roles
from dsd.services.historical_data_service import post_historical_data_element_values_to_dhis2
from dsd.services.sync_cocid_service import set_coc_id

logger = logging.getLogger(__name__)


def sync_metadata_with_bes():
    sync_metadata_to_local()
    sync_business_data_to_local()
    if SyncRecord.objects.filter(status='Success').count() == 1:
        logger.info('push metadata and data to DHIS2 start...')
        sync_metadata_and_data_with_dhis2()
        logger.info('push metadata and data to DHIS2 end...')


def sync_metadata_and_data_with_dhis2():
    post_attributes()
    post_organization_units()
    post_category_options()
    post_categories()
    post_category_combinations()
    post_elements()
    post_data_set()
    set_coc_id()
    post_all_validation_rule_and_group()
    assign_all_org_to_user()
    set_org_unit_level()
    set_user_roles()
    sync_business_with_dhis2()
    post_historical_data_element_values_to_dhis2()


def sync_business_with_dhis2():
    date_element_values = fetch_updated_data_element_values()
    post_data_element_values(date_element_values)


def need_sync_bes_data():
    return not SyncRecord.objects.filter(status='Success').count()


def sync_trigger():
    while need_sync_bes_data():
        sync_metadata_with_bes()


sync_trigger()
