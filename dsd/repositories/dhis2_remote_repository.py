import logging

from dsd.models import Attribute
from dsd.models import Element
from dsd.models.moh import MoH
from dsd.repositories.dhis2_oauth_token import *
from dsd.repositories.request_template.add_attribute_template import AddAttributeRequestTemplate
from dsd.repositories.request_template.add_element_template import AddElementRequestTemplate

CONTENT_TYPE = {'Content-Type': 'application/json'}

logger = logging.getLogger(__name__)


def add_data_set_elements_value(request_body):
    return __post_request(url=dhis2_config.DHIS2_URLS.get(dhis2_config.KEY_ADD_DATA_SET_ELEMENTS), data=request_body)


def add_organization_unit(request_body):
    return __post_request(url=dhis2_config.DHIS2_URLS.get(dhis2_config.KEY_ADD_ORGANIZATION_UNIT), data=request_body)


def add_attribute(request_body):
    return __post_request(url=dhis2_config.DHIS2_URLS.get(dhis2_config.KEY_ADD_ATTRIBUTE), data=request_body)


def add_element(request_body):
    return __post_request(url=dhis2_config.DHIS2_URLS.get(dhis2_config.KEY_ADD_ELEMENT), data=request_body)


def __post_request(url, data):
    try:
        return requests.post(url=url,
                             data=data,
                             headers=get_oauth_header(),
                             verify=settings.DHIS2_SSL_VERIFY)
    except ConnectionError:
        raise RemoteRequestException()


def add_data_set(request_body):
    return __post_request(url=dhis2_config.DHIS2_URLS.get(dhis2_config.KEY_ADD_DATA_SET), data=request_body)


def post_attributes():
    attributes = Attribute.objects.all()
    for attribute in attributes:
        request_body_dict = AddAttributeRequestTemplate().build(uid=attribute.uid,
                                                                code=attribute.code,
                                                                value_type=attribute.value_type,
                                                                org_unit_attr=attribute.org_unit_attr,
                                                                name=attribute.name)
        response = add_attribute(json.dumps(request_body_dict))
        logger.info("response status = %s" % response.status_code)


def post_elements():
    category_combo_id = dhis2_config.CATEGORY_COMBO_ID
    elements = Element.objects.all()
    for element in elements:
        request_body_dict = AddElementRequestTemplate().build(id=element.id,
                                                              code=element.code,
                                                              value_type=element.value_type,
                                                              short_name=element.short_name,
                                                              domain_type=element.domain_type,
                                                              category_combo=category_combo_id,
                                                              name=element.name)
        response = add_element(json.dumps(request_body_dict))
        logger.info("response status = %s" % response.status_code)


def post_organization_units():
    # TODO: filter by sync time
    organization_units = MoH().get_organization_as_list()
    for organization_unit in organization_units:
        logger.info("response unit = %s" % organization_unit)
        response = add_organization_unit(json.dumps(organization_unit))
        logger.info("response status = %s" % response.status_code)


def get_oauth_header():
    return {'Authorization': 'bearer %s' % get_access_token(), 'Content-Type': 'application/json'}
