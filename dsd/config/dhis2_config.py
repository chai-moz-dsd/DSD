# DHIS2 configuration

VERSION = 24

DHIS2_BASE_URL = 'http://52.32.36.132/'

KEY_ADD_ATTRIBUTE = 'add_attribute'
KEY_ADD_ELEMENT = 'add_element'
KEY_ADD_ORGANIZATION_UNIT = 'add_organization_unit'
KEY_ADD_DATA_SET_ELEMENTS = 'add_data_set_elements'
KEY_ADD_DATA_SET = 'add_data_set'
OAUTH2_TOKEN = 'oauth2_token'
OAUTH2_CREATE = 'oauth2_create'

DHIS2_URLS = {
    KEY_ADD_ATTRIBUTE: "%sapi/%s/attributes" % (DHIS2_BASE_URL, VERSION),
    KEY_ADD_ORGANIZATION_UNIT: '%sapi/%s/organisationUnits' % (DHIS2_BASE_URL, VERSION),
    KEY_ADD_DATA_SET_ELEMENTS: '%sapi/%s/dataValueSets' % (DHIS2_BASE_URL, VERSION),
    KEY_ADD_ELEMENT: '%sapi/%s/dataElements' % (DHIS2_BASE_URL, VERSION),
    KEY_ADD_DATA_SET: '%sapi/%s/dataSets' % (DHIS2_BASE_URL, VERSION),
    OAUTH2_TOKEN: "%suaa/oauth/token" % DHIS2_BASE_URL,
    OAUTH2_CREATE: "%sapi/oAuth2Clients" % DHIS2_BASE_URL,
}

CATEGORY_COMBO_ID = '84jf8wld02d'
DATA_SET_ID = '84ndl9jeldu'
DATA_SET_NAME = 'chai_disease'
DATA_SET_PERIOD_TYPES = 'Weekly'
