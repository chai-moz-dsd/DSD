# DHIS2 configuration
import os

VERSION = 24
DHIS2_PORT_8080_TCP_ADDR = os.environ.get('DHIS2_PORT_8080_TCP_ADDR','10.0.0.1')
DHIS2_PORT_8080_TCP_PORT = os.environ.get('DHIS2_PORT_8080_TCP_PORT','8080')
os.environ.get('KEY_THAT_MIGHT_EXIST')
DHIS2_BASE_URL = 'http://%s:%s'% (DHIS2_PORT_8080_TCP_ADDR, DHIS2_PORT_8080_TCP_PORT)

KEY_POST_ATTRIBUTE = '_post_attribute'
KEY_POST_ELEMENT = '_post_element'
KEY_POST_ORGANIZATION_UNIT = '_post_organization_unit'
KEY_POST_DATA_SET_ELEMENTS = '_post_data_set_elements'
KEY_POST_DATA_SET = '_post_data_set'
KEY_POST_CATEGORY_OPTIONS = '_post_category_options'
KEY_POST_CATEGORIES = '_post_categories'
KEY_POST_CATEGORY_COMBINATIONS = '_post_category_combinations'
KEY_GET_SELF_PROFILE = '_get_self_profile'
OAUTH2_TOKEN = 'oauth2_token'
OAUTH2_CREATE = 'oauth2_create'

DHIS2_STATIC_URLS = {
    KEY_POST_ATTRIBUTE: '%sapi/%s/attributes' % (DHIS2_BASE_URL, VERSION),
    KEY_POST_ORGANIZATION_UNIT: '%sapi/%s/organisationUnits' % (DHIS2_BASE_URL, VERSION),
    KEY_POST_DATA_SET_ELEMENTS: '%sapi/%s/dataValueSets' % (DHIS2_BASE_URL, VERSION),
    KEY_POST_ELEMENT: '%sapi/%s/dataElements' % (DHIS2_BASE_URL, VERSION),
    KEY_POST_DATA_SET: '%sapi/%s/dataSets' % (DHIS2_BASE_URL, VERSION),
    KEY_POST_CATEGORY_OPTIONS: '%sapi/%s/categoryOptions' % (DHIS2_BASE_URL, VERSION),
    KEY_POST_CATEGORIES: '%sapi/%s/categories' % (DHIS2_BASE_URL, VERSION),
    KEY_POST_CATEGORY_COMBINATIONS: '%sapi/%s/categoryCombos' % (DHIS2_BASE_URL, VERSION),
    KEY_GET_SELF_PROFILE: '%sapi/%s/me' % (DHIS2_BASE_URL, VERSION),
    OAUTH2_TOKEN: '%suaa/oauth/token' % DHIS2_BASE_URL,
    OAUTH2_CREATE: '%sapi/oAuth2Clients' % DHIS2_BASE_URL,
}

DATA_SET_ID = 'TTLoO39Scy9'
DATA_SET_NAME = 'chai_disease'
DATA_SET_PERIOD_TYPES = 'Weekly'

CATEGORY_DATA_DIMENSION = True
CATEGORY_DATA_DIMENSION_TYPE = 'DISAGGREGATION'


def key_get_cocid(category_comb_id):
    return '%sapi/%s/categoryCombos/%s?fields=categoryOptionCombos[id,name]' % (
        DHIS2_BASE_URL, VERSION, category_comb_id)


def key_update_user(user_id):
    return '%sapi/%s/users/%s' % (DHIS2_BASE_URL, VERSION, user_id)
