from dsd.repositories.dhis2_oauth_token import create_oauth
from dsd.services.dhis2_remote_service import *
from dsd.services.sync_cocid_service import set_coc_id

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
post_data_element_values()
