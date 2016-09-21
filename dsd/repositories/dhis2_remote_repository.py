from dsd.repositories.dhis2_oauth_token import *

CONTENT_TYPE = {'Content-Type': 'application/json'}

logger = logging.getLogger(__name__)


def post_category_options(request_body):
    return __post_request(url=dhis2_config.DHIS2_STATIC_URLS.get(dhis2_config.KEY_POST_CATEGORY_OPTIONS),
                          data=request_body)


def post_category_combinations(request_body):
    return __post_request(url=dhis2_config.DHIS2_STATIC_URLS.get(dhis2_config.KEY_POST_CATEGORY_COMBINATIONS),
                          data=request_body)


def post_categories(request_body):
    return __post_request(url=dhis2_config.DHIS2_STATIC_URLS.get(dhis2_config.KEY_POST_CATEGORIES), data=request_body)


def post_data_elements_value(request_body):
    return __post_request(url=dhis2_config.DHIS2_STATIC_URLS.get(dhis2_config.KEY_POST_DATA_SET_ELEMENTS),
                          data=request_body)


def post_organization_unit(request_body):
    return __post_request(url=dhis2_config.DHIS2_STATIC_URLS.get(dhis2_config.KEY_POST_ORGANIZATION_UNIT),
                          data=request_body)


def post_attribute(request_body):
    return __post_request(url=dhis2_config.DHIS2_STATIC_URLS.get(dhis2_config.KEY_POST_ATTRIBUTE), data=request_body)


def post_element(request_body):
    return __post_request(url=dhis2_config.DHIS2_STATIC_URLS.get(dhis2_config.KEY_POST_ELEMENT), data=request_body)


def post_data_set(request_body):
    return __post_request(url=dhis2_config.DHIS2_STATIC_URLS.get(dhis2_config.KEY_POST_DATA_SET), data=request_body)


def post_to_set_org_level(request_body):
    return __post_request(url=dhis2_config.DHIS2_STATIC_URLS.get(dhis2_config.KEY_SET_ORG_LEVEL), data=request_body)


def get_data_element_values(query_params):
    url = '%s?%s' % (dhis2_config.DHIS2_STATIC_URLS.get(dhis2_config.KEY_GET_DATA_ELEMENT_VALUES), query_params)
    return requests.get(url=url, headers=get_oauth_header(), verify=settings.DHIS2_SSL_VERIFY)


def get_self_profile():
    header = {'Authorization': 'bearer %s' % get_access_token()}
    response = requests.get(url=dhis2_config.DHIS2_STATIC_URLS.get(dhis2_config.KEY_GET_SELF_PROFILE),
                            headers=header,
                            verify=settings.DHIS2_SSL_VERIFY)
    return response.text


def update_user(request_body, user_id):
    return requests.put(url=dhis2_config.key_update_user(user_id),
                        data=request_body,
                        headers=get_oauth_header(),
                        verify=settings.DHIS2_SSL_VERIFY)


def __post_request(url, data):
    try:
        return requests.post(url=url,
                             data=data,
                             headers=get_oauth_header(),
                             verify=settings.DHIS2_SSL_VERIFY)
    except ConnectionError:
        raise RemoteRequestException()


def get_oauth_header():
    return {'Authorization': 'bearer %s' % get_access_token(), 'Content-Type': 'application/json'}
