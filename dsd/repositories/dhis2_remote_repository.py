import requests
from django.conf import settings

from dsd.exceptions.remote_request_exception import RemoteRequestException

CONTENT_TYPE = {"Content-Type": "application/json"}
HEADER_DHIS2 = {'Authorization': 'Token %s' % settings.DHIS2_API_TOKEN, "Content-Type": "application/json"}


def add_data_set_elements(request_body):
    return __post_request(url=settings.DHIS2_URLS.get(settings.KEY_ADD_DATA_SET_ELEMENTS), data=request_body)


def add_organization_unit(request_body):
    return __post_request(url=settings.DHIS2_URLS.get(settings.KEY_ADD_ORGANIZATION_UNIT), data=request_body)


def add_attribute(request_body):
    return __post_request(url=settings.DHIS2_URLS.get(settings.KEY_ADD_ATTRIBUTE), data=request_body)


def add_attribute_to_schemas(request_body):
    return __post_request(url=settings.DHIS2_URLS.get(settings.KEY_ADD_ATTRIBUTE_TO_SCHEMAS), data=request_body)


def __post_request(url, data):
    try:
        return requests.post(url=url,
                             data=data,
                             headers=HEADER_DHIS2,
                             verify=settings.DHIS2_SSL_VERIFY)
    except ConnectionError:
        raise RemoteRequestException()


def parse_attributes(attributes_list):
    for attribute in attributes_list:
        # validation
        add_attribute(attribute)
