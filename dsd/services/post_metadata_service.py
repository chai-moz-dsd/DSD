import logging

from dsd.models import SyncRecord
from dsd.scheduler import sync_business_data_to_local
from dsd.services.dhis2_remote_service import post_attributes, post_organization_units, post_category_options, post_categories, post_category_combinations, post_elements, post_data_set, assign_all_org_to_user, set_org_unit_level
# from dsd.services.historical_data_service import post_historical_data_element_values_to_dhis2
from dsd.services.sync_cocid_service import set_coc_id

logger = logging.getLogger(__name__)


def sync_metadata_with_bes():
    sync_business_data_to_local()
    if SyncRecord.objects.filter(status='Success').count() == 1:
        logger.info('Sync metadata start...')
        sync_metadata_with_dhis2()
        logger.info('Sync metadata end...')


def sync_metadata_with_dhis2():
    post_attributes()
    post_organization_units()
    post_category_options()
    post_categories()
    post_category_combinations()
    post_elements()
    post_data_set()
    set_coc_id()
    assign_all_org_to_user()
    set_org_unit_level()
    # post_historical_data_element_values_to_dhis2()


def need_sync_bes_data():
    return not SyncRecord.objects.filter(status='Success').count()


while need_sync_bes_data():
    sync_metadata_with_bes()
