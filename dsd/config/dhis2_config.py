# DHIS2 configuration
import os

VERSION = 24
DHIS2_1_ENV_DOCKERCLOUD_SERVICE_FQDN = os.environ.get('DHIS2_1_ENV_DOCKERCLOUD_SERVICE_FQDN', '52.32.36.132')
DHIS2_BASE_URL = 'http://%s:%s/' % (DHIS2_1_ENV_DOCKERCLOUD_SERVICE_FQDN, '80')

KEY_POST_ATTRIBUTE = '_post_attribute'
KEY_POST_ELEMENT = '_post_element'
KEY_POST_ORGANIZATION_UNIT = '_post_organization_unit'
KEY_POST_DATA_SET_ELEMENTS = '_post_data_set_elements'
KEY_POST_DATA_SET = '_post_data_set'
KEY_POST_CATEGORY_OPTIONS = '_post_category_options'
KEY_POST_CATEGORIES = '_post_categories'
KEY_POST_CATEGORY_COMBINATIONS = '_post_category_combinations'
KEY_SET_ORG_LEVEL = '_set_org_level'
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
    KEY_SET_ORG_LEVEL: '%sapi/%s/filledOrganisationUnitLevels' % (DHIS2_BASE_URL, VERSION),
    KEY_GET_SELF_PROFILE: '%sapi/%s/me' % (DHIS2_BASE_URL, VERSION),
    OAUTH2_TOKEN: '%suaa/oauth/token' % DHIS2_BASE_URL,
    OAUTH2_CREATE: '%sapi/oAuth2Clients' % DHIS2_BASE_URL,
}

DATA_SET_ID = 'TTLoO39Scy9'
DATA_SET_NAME = 'chai_disease'
DATA_SET_PERIOD_TYPES = 'Weekly'

CATEGORY_DATA_DIMENSION = True
CATEGORY_DATA_DIMENSION_TYPE = 'DISAGGREGATION'

ONE_WEEK_DAYS = 6
THREE_WEEKS_DAYS = 20
FOUR_WEEKS_DAYS = 27
FIVE_WEEKS_DAYS = 34
SARAMPO_IN_A_MONTH_THRESHOLD = 5
DISEASE_I18N_MAP = {
    'measles': 'SARAMPO',
    'tetanus': 'T&Eacute;TANO REC&Eacute;M NASCIDOS',
    'malaria': 'MAL&Aacute;RIA',
    'pfa': 'PARALISIA FL&Aacute;CIDA AGUDA',
    'rabies': 'RAIVA',
    'diarrhea': 'DIARREIA',
    'dysentery': 'DISENTERIA',
    'cholera': 'C&Oacute;LERA',
    'plague': 'PESTE',
    'meningitis': 'MENINGITE',
}


def key_get_cocid(category_comb_id):
    return '%sapi/%s/categoryCombos/%s?fields=categoryOptionCombos[id,name]' % (
        DHIS2_BASE_URL, VERSION, category_comb_id)


def key_update_user(user_id):
    return '%sapi/%s/users/%s' % (DHIS2_BASE_URL, VERSION, user_id)
