from dsd import scheduler
from dsd.models import SyncRecord
from dsd.repositories.dhis2_oauth_token import *
from dsd.services.dhis2_remote_service import *
from dsd.services.sync_cocid_service import set_coc_id

logger = logging.getLogger(__name__)

def sync_metadata_with_bes():
    scheduler.start()
    logger.info('Sync metadata start...')
    sync_metadata_with_dhis2()

def sync_metadata_with_dhis2():
    if (SyncRecord.objects.filter(status='Success').count() == 1):
        logger.info('INITIAL UPLOAD METADATA...')
        initial_access_token()
        post_attributes()
        post_organization_units()
        post_category_options()
        post_categories()
        post_category_combinations()
        post_elements()
        post_data_set()
        set_coc_id()
        assign_all_org_to_user()
        post_data_element_values()
    if (SyncRecord.objects.filter(status='Success').count() == 0):
        sync_metadata_with_bes()

sync_metadata_with_bes()