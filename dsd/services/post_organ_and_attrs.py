from dsd.repositories.dhis2_oauth_token import create_oauth
from dsd.services.dhis2_remote_service import  post_attributes, post_elements

create_oauth()
post_attributes()
post_elements()
