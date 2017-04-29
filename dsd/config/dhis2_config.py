# DHIS2 configuration

# URL config
from django.conf import settings

VERSION = 24
# DHIS2_BASE_URL = 'http://%s:%s/' % (settings.DHIS2_SERVER_IP, settings.DHIS2_PORT)
DHIS2_BASE_URL = 'https://%s/' % settings.DHIS2_SERVER_IP

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
KEY_GET_DATA_ELEMENT_VALUES = '_get_data_element_values'
KEY_GET_VALIDATION_RULES = '_key_get_validation_rules'
KEY_GET_VALIDATION_RULE_GROUPS = '_key_get_validation_rule_groups'
KEY_RUN_VALIDATION_ACTION = '_key_run_validation_action'
KEY_SEND_ANALYSIS_ACTION = '_key_send_analysis_action'
KEY_POST_METADATA = '_key_post_metadata'
KEY_GET_ORGANISATIONUNITS = '_get_organisationunits'
KEY_POST_USER_ROLES = '_post_user_roles'
KEY_POST_USER_GROUPS = '_post_user_groups'
KEY_GET_USER_GROUPS = KEY_POST_USER_GROUPS
KEY_POST_SYSTEM_SETTINGS = '_post_system_settings'
KEY_POST_ALERT_CONFIG = '_post_alert_config'

OAUTH2_TOKEN = 'oauth2_token'
OAUTH2_CREATE = 'oauth2_create'

HEADER_OAUTH = {'Accept': 'application/json'}
HEADERS_CONTENT_TYPE_APPLICATION_JSON = {'Content-Type': 'application/json'}
HEADERS_CONTENT_TYPE_APPLICATION_XML = {'Content-Type': 'application/xml'}
USERNAME = settings.USERNAME
PASSWORD = settings.PASSWORD
# OAUTH2_UID = settings.OAUTH2_UID
# OAUTH2_SECRET = settings.OAUTH2_SECRET
ACCESS_TOKEN = 'access_token'
REFRESH_TOKEN = 'refresh_token'
EXPIRES_TIME = 36000

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
    KEY_GET_DATA_ELEMENT_VALUES: '%sapi/%s/analytics' % (DHIS2_BASE_URL, VERSION),
    KEY_GET_VALIDATION_RULES: '%sapi/%s/validationRules' % (DHIS2_BASE_URL, VERSION),
    KEY_SEND_ANALYSIS_ACTION: '%sdhis-web-reporting/startExport.action' % DHIS2_BASE_URL,
    KEY_GET_VALIDATION_RULE_GROUPS: '%sdhis-web-validationrule/validationRuleGroup.action' % DHIS2_BASE_URL,
    KEY_RUN_VALIDATION_ACTION: '%sdhis-web-validationrule/runValidationAction.action' % DHIS2_BASE_URL,
    KEY_POST_METADATA: '%sapi/metaData' % DHIS2_BASE_URL,
    KEY_GET_ORGANISATIONUNITS: '%sapi/organisationUnits' % DHIS2_BASE_URL,
    KEY_POST_USER_ROLES: '%sapi/%s/userRoles' % (DHIS2_BASE_URL, VERSION),
    KEY_POST_USER_GROUPS: '%sapi/%s/userGroups' % (DHIS2_BASE_URL, VERSION),
    KEY_POST_SYSTEM_SETTINGS: '%sapi/%s/systemSettings' % (DHIS2_BASE_URL, VERSION),
    KEY_POST_ALERT_CONFIG: '%sapi/%s/alertConfiguration/setDefault' % (DHIS2_BASE_URL, VERSION)
}

DATA_SET_ID = 'TTLoO39Scy9'
DATA_SET_NAME = 'chai_disease'
DATA_SET_PERIOD_TYPES = 'Weekly'

CATEGORY_DATA_DIMENSION = True
CATEGORY_DATA_DIMENSION_TYPE = 'DISAGGREGATION'

ONE_WEEK_DAYS = 7
THREE_WEEKS_DAYS = 21
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

MEASLES_CASES = '_measles_cases_in_recent_epi_weeks'
MENINGITIS_CASES = '_meningitis_cases_increases_by_times_in_recent_consecutive_weeks'
DYSENTERY_CASES = '_dysentery_cases_surpass_average_for_same_week_in_last_years_by_std_dev'
MALARIA_CASES = '_malaria_cases_surpass_average_from_current_week_earlier_weeks_to_later_weeks_in_past_years_by_std_dev'

CUSTOMIZED_VALIDATION_RULE_TYPE = {
    MEASLES_CASES: 'SarampoCaseInMonths',
    MENINGITIS_CASES: 'MeningiteIncreasedInWeeks',
    DYSENTERY_CASES: 'DisenteriaCaseInYears',
    MALARIA_CASES: 'MalariaCaseInYears',
}

CUSTOMIZED_VALIDATION_RULE_TYPE_PARAMS_REGEX = {
    CUSTOMIZED_VALIDATION_RULE_TYPE.get(MEASLES_CASES): r'([A-B]):(\d+)([A-B]):(\d+)',
    CUSTOMIZED_VALIDATION_RULE_TYPE.get(MENINGITIS_CASES): r'([A-B]):(\d+)([A-B]):(\d+)',
    CUSTOMIZED_VALIDATION_RULE_TYPE.get(DYSENTERY_CASES): r'([A-B]):(\d+)([A-B]):(\d+)',
    CUSTOMIZED_VALIDATION_RULE_TYPE.get(MALARIA_CASES): r'([A-D]):(\d+)([A-D]):(\d+)([A-D]):(\d+)([A-D]):(\d+)',
}

CUSTOMIZED_VALIDATION_RULE_TYPE_PARAMS_REPLACEMENT = {
    CUSTOMIZED_VALIDATION_RULE_TYPE.get(MEASLES_CASES): '{\"\\1\":\\2,\"\\3\":\\4}',
    CUSTOMIZED_VALIDATION_RULE_TYPE.get(MENINGITIS_CASES): '{\"\\1\":\\2,\"\\3\":\\4}',
    CUSTOMIZED_VALIDATION_RULE_TYPE.get(DYSENTERY_CASES): '{\"\\1\":\\2,\"\\3\":\\4}',
    CUSTOMIZED_VALIDATION_RULE_TYPE.get(MALARIA_CASES): '{\"\\1\":\\2,\"\\3\":\\4,\"\\5\":\\6,\"\\7\":\\8}',
}

CUSTOMIZED_VALIDATION_RULE_TYPE_PARAMS = {
    CUSTOMIZED_VALIDATION_RULE_TYPE.get(MEASLES_CASES): {'recent_weeks': 'A', 'threshold': 'B'},
    CUSTOMIZED_VALIDATION_RULE_TYPE.get(MENINGITIS_CASES): {'times': 'A', 'recent_weeks': 'B'},
    CUSTOMIZED_VALIDATION_RULE_TYPE.get(DYSENTERY_CASES): {'recent_years': 'A', 'std_dev': 'B'},
    CUSTOMIZED_VALIDATION_RULE_TYPE.get(MALARIA_CASES): {'weeks_before': 'A', 'weeks_after': 'B', 'recent_years': 'C',
                                                         'std_dev': 'D'},
}

VALIDATION_RULE_GROUP = {'tOCXddkXkw0': {'group_id': 'ahkz0JjYY3U', 'name': 'Cólera grupo'},
                         'iz4ccOJSd4l': {'group_id': 'Tk0L27C81tj', 'name': 'Cólera morte grupo'},
                         'NGNXRZoeBgj': {'group_id': 'FGVVEJ2rQaQ', 'name': 'Diarreia adulto death Case grupo'},
                         'QhVKtePYsLu': {'group_id': 'g0AWTpbBv2o', 'name': 'Disenteria (Shigella): Caso > 0 grupo'},
                         'GzblVtRJAQD': {'group_id': 'rBCKKqjIuuR', 'name': 'Paralesia flacida aguda (PFA) > 0 grupo'},
                         'MlHtb3yxsJn': {'group_id': 'mrAYBxgnXfE', 'name': 'Peste caso > 0 grupo'},
                         'SBm9jfYqwFc': {'group_id': 'e1pmwU7g6Xs', 'name': 'Raiva caso > 0 grupo'},
                         'AhTAFtw7sM4': {'group_id': 'DroI496nwkw', 'name': 'Raiva morte > 0 grupo'},
                         'C0U9HaMlefd': {'group_id': 'L72yTgEawjF', 'name': 'Sarampo case in a HF in a week grupo'},
                         'Q9Ko2HFaPJm': {'group_id': 'z42zF2yCkUv', 'name': 'Tétano no recém nascido caso > 0 grupo'},
                         'm9vqJzIXCcr': {'group_id': 'VcKxBPAsrC4',
                                         'name': 'Malária: Casos > average from current week + (A) ealiar weeks to current week - (B) weeks later weeks in past (C)years + (D) * std dev grupo'},
                         'vKERgxn2ycf': {'group_id': 'hObttGvUJOE',
                                         'name': 'Disenteria: Cases > average for same week in last ( A ) years + ( B ) * std dev grupo'},
                         'JTiPI2lUKp0': {'group_id': 'rkreV2RQAoY',
                                         'name': 'Meningite (inclui suspeitas) week1 < week2 * 2 < week3 * 2 grupo'},
                         'FU31nh8lfLn': {'group_id': 'L23BjGdJeKD', 'name': 'Sarampo case in a district a month grupo'}}

USER_ROLE_NAME = 'Data Viewer'
ADMIN_ID = 'M5zQapPyTZI'

USER_ROLE_AUTH_PROPS = [
    'F_USER_VIEW',
    'M_dhis-web-dataentry',
    'M_dhis-web-pivot',
    'M_dhis-web-usage-analytics',
    'M_dhis-web-validationrule',
    'M_dhis-web-maintenance-dataset',
    'F_USERROLE_LIST',
    'F_RUN_VALIDATION',
    'M_dhis-web-light',
    'M_dhis-web-importexport',
    'M_reporting-page',
    'M_dhis-web-settings',
    'M_dhis-web-maintenance-mobile',
    'F_VIEW_DATABROWSER',
    'M_dhis-web-api-fred',
    'M_dhis-web-tracker-capture',
    'M_dhis-web-event-capture',
    'M_dhis-web-sms',
    'M_dhis-web-visualizer',
    'M_dhis-web-maintenance-user',
    'M_dhis-web-reporting',
    'M_dhis-web-maintenance-dataadmin',
    'M_dhis-web-event-reports',
    'F_VIEW_UNAPPROVED_DATA',
    'M_dhis-web-mobile',
    'M_dhis-web-maintenance',
    'F_USERGROUP_MANAGING_RELATIONSHIPS_VIEW',
    'M_dhis-web-dashboard-integration',
    'M_dhis-web-cache-cleaner',
    'M_dhis-web-event-visualizer',
    'F_USER_ADD',
    'M_dhis-web-app-management',
    'M_dhis-web-maintenance-program',
    'M_dhis-web-mapping'
]


def key_get_cocid(category_comb_id):
    return '%sapi/%s/categoryCombos/%s?fields=categoryOptionCombos[id,name]' % (
        DHIS2_BASE_URL, VERSION, category_comb_id)


def key_update_user(user_id):
    return '%sapi/%s/users/%s' % (DHIS2_BASE_URL, VERSION, user_id)
