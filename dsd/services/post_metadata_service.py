from dsd.models import SyncRecord
from dsd.repositories.dhis2_oauth_token import *
from dsd.scheduler import sync_remote_data_to_local
from dsd.services.dhis2_remote_service import *
from dsd.services.sync_cocid_service import set_coc_id

logger = logging.getLogger(__name__)


def sync_metadata_with_bes():
    sync_remote_data_to_local()

    if SyncRecord.objects.filter(status='Success').count() == 1:
        logger.info('Sync metadata start...')
        sync_metadata_with_dhis2()


def sync_metadata_with_dhis2():
    create_oauth()
    post_attributes()
    post_organization_units()
    post_category_options()
    post_categories()
    post_category_combinations()
    post_elements()
    post_data_set()
    set_coc_id()
    assign_all_org_to_user()


def need_sync_bes_data():
    return not SyncRecord.objects.filter(status='Success').count()


while need_sync_bes_data():
    sync_metadata_with_bes()
