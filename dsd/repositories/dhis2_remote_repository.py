import requests
from django.conf import settings

from dsd.exceptions.remote_request_exception import RemoteRequestException

CONTENT_TYPE = {"Content-Type": "application/json"}
HEADER_DHIS2 = {'Authorization': 'Token %s' % settings.DHIS2_API_TOKEN, "Content-Type": "application/json"}


def add_organization_unit(request_body):
    try:
        return requests.post(url=settings.DHIS2_URLS.get(settings.KEY_ADD_ORGANIZATION_UNIT),
                             data=request_body,
                             headers=HEADER_DHIS2,
                             verify=settings.DHIS2_SSL_VERIFY)
    except ConnectionError:
        raise RemoteRequestException()


def add_attribute(request_body):
    try:
        return requests.post(url=settings.DHIS2_URLS.get(settings.KEY_ADD_ATTRIBUTE),
                             data=request_body,
                             headers=HEADER_DHIS2,
                             verify=settings.DHIS2_SSL_VERIFY)
    except ConnectionError:
        raise RemoteRequestException()


def add_attribute_to_schemas(request_body):
    try:
        return requests.post(url=settings.DHIS2_URLS.get(settings.KEY_ADD_ATTRIBUTE_TO_SCHEMAS),
                             data=request_body,
                             headers=HEADER_DHIS2,
                             verify=settings.DHIS2_SSL_VERIFY)
    except ConnectionError:
        raise RemoteRequestException()


def parse_attributes(attributes_list):
    for attribute in attributes_list:
        # validation
        add_attribute(attribute)
