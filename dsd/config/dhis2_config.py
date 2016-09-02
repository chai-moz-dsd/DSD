# DHIS2 configuration

VERSION = 24

DHIS2_BASE_URL = 'http://52.32.36.132/'

KEY_POST_ATTRIBUTE = '_post_attribute'
KEY_POST_ELEMENT = '_post_element'
KEY_POST_ORGANIZATION_UNIT = '_post_organization_unit'
KEY_POST_DATA_SET_ELEMENTS = '_post_data_set_elements'
KEY_POST_DATA_SET = '_post_data_set'
KEY_POST_CATEGORY_OPTIONS = '_post_category_options'
KEY_POST_CATEGORIES = '_post_categories'
KEY_POST_CATEGORY_COMBINATIONS = '_post_category_combinations'
OAUTH2_TOKEN = 'oauth2_token'
OAUTH2_CREATE = 'oauth2_create'

DHIS2_URLS = {
    KEY_POST_ATTRIBUTE: "%sapi/%s/attributes" % (DHIS2_BASE_URL, VERSION),
    KEY_POST_ORGANIZATION_UNIT: '%sapi/%s/organisationUnits' % (DHIS2_BASE_URL, VERSION),
    KEY_POST_DATA_SET_ELEMENTS: '%sapi/%s/dataValueSets' % (DHIS2_BASE_URL, VERSION),
    KEY_POST_ELEMENT: '%sapi/%s/dataElements' % (DHIS2_BASE_URL, VERSION),
    KEY_POST_DATA_SET: '%sapi/%s/dataSets' % (DHIS2_BASE_URL, VERSION),
    KEY_POST_CATEGORY_OPTIONS: '%sapi/%s/categoryOptions' % (DHIS2_BASE_URL, VERSION),
    KEY_POST_CATEGORIES: '%sapi/%s/categories' % (DHIS2_BASE_URL, VERSION),
    KEY_POST_CATEGORY_COMBINATIONS: '%sapi/%s/categoryCombos' % (DHIS2_BASE_URL, VERSION),
    OAUTH2_TOKEN: "%suaa/oauth/token" % DHIS2_BASE_URL,
    OAUTH2_CREATE: "%sapi/oAuth2Clients" % DHIS2_BASE_URL,
}

CATEGORY_COMBO_ID = '84jf8wld02d'
DATA_SET_ID = '84ndl9jeldu'
DATA_SET_NAME = 'chai_disease'
DATA_SET_PERIOD_TYPES = 'Weekly'
