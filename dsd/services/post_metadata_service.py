from dsd.repositories.dhis2_oauth_token import create_oauth
from dsd.services.dhis2_remote_service import post_attributes, post_organization_units, post_elements, \
    post_category_options, post_categories, post_category_combinations, post_data_set, update_user
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

update_user()
