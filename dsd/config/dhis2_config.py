# DHIS2 configuration
import os

# URL config
VERSION = 24
DHIS2_1_ENV_DOCKERCLOUD_SERVICE_FQDN = os.environ.get('SERVER_IP_ADDRESS', '52.32.36.132')
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
KEY_GET_DATA_ELEMENT_VALUES = '_get_data_element_values'
KEY_GET_VALIDATION_RULES = '_key_get_validation_rules'
KEY_GET_VALIDATION_RULE_GROUPS = '_key_get_validation_rule_groups'
KEY_RUN_VALIDATION_ACTION = '_key_run_validation_action'

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
    KEY_GET_DATA_ELEMENT_VALUES: '%sapi/%s/analytics' % (DHIS2_BASE_URL, VERSION),
    KEY_GET_VALIDATION_RULES: '%sapi/%s/validationRules' % (DHIS2_BASE_URL, VERSION),
    OAUTH2_TOKEN: '%suaa/oauth/token' % DHIS2_BASE_URL,
    OAUTH2_CREATE: '%sapi/oAuth2Clients' % DHIS2_BASE_URL,
    KEY_GET_VALIDATION_RULE_GROUPS: '%sdhis-web-validationrule/validationRuleGroup.action' % DHIS2_BASE_URL,
    KEY_RUN_VALIDATION_ACTION: '%sdhis-web-validationrule/runValidationAction.action' % DHIS2_BASE_URL,
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
    DYSENTERY_CASES: 'DiarrieaCaseInYears',
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


def key_get_cocid(category_comb_id):
    return '%sapi/%s/categoryCombos/%s?fields=categoryOptionCombos[id,name]' % (
        DHIS2_BASE_URL, VERSION, category_comb_id)


def key_update_user(user_id):
    return '%sapi/%s/users/%s' % (DHIS2_BASE_URL, VERSION, user_id)
