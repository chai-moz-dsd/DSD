import json
import logging

from dsd.config import dhis2_config
from dsd.models import Attribute
from dsd.models import Element
from dsd.models.moh import MoH
from dsd.repositories import dhis2_remote_repository
from dsd.repositories.dhis2_remote_repository import add_attribute, add_element, add_organization_unit
from dsd.repositories.request_template.add_element_template import AddElementRequestTemplate
from dsd.services.attribute_service import convert_attribute_to_dict
from dsd.services.bes_middleware_core_service import build_data_set_request_body_as_dict

logger = logging.getLogger(__name__)


def post_attributes():
    attributes = Attribute.objects.all()
    for attribute in attributes:
        request_body_dict = convert_attribute_to_dict(attribute)
        logger.info(request_body_dict)
        response = add_attribute(json.dumps(request_body_dict))
        logger.info("response status = %s" % response.status_code)


def post_organization_units():
    organization_units = MoH().get_organization_as_list()
    for organization_unit in organization_units:
        logger.info("response unit = %s" % organization_unit)
        response = add_organization_unit(json.dumps(organization_unit))
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
                                                              aggregation_type=element.aggregation_type,
                                                              name=element.name)
        response = add_element(json.dumps(request_body_dict))
        logger.info("response status = %s" % response)


def post_data_set():
    dhis2_remote_repository.post_data_set(json.dumps(build_data_set_request_body_as_dict()))
