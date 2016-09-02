import json
import logging
from datetime import datetime

from dsd.config import dhis2_config
from dsd.models import Attribute
from dsd.models import BesMiddlewareCore
from dsd.models import Element
from dsd.models import SyncRecord
from dsd.models.moh import MoH
from dsd.models import Facility
from dsd.repositories import dhis2_remote_repository
from dsd.repositories.dhis2_remote_repository import post_attribute
from dsd.repositories.dhis2_remote_repository import post_element, post_organization_unit
from dsd.repositories.request_template.add_element_template import AddElementRequestTemplate

logger = logging.getLogger(__name__)


def post_attributes():
    attributes = Attribute.objects.all()
    for attribute in attributes:
        request_body_dict = convert_attribute_to_dict(attribute)
        logger.info(request_body_dict)
        response = post_attribute(json.dumps(request_body_dict))
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
        response = post_element(json.dumps(request_body_dict))
        logger.info("response status = %s" % response)


def post_organization_units():
    organization_units = MoH().get_organization_as_list()
    for organization_unit in organization_units:
        logger.info("response unit = %s" % organization_unit)
        response = post_organization_unit(json.dumps(organization_unit))
        logger.info("response status = %s" % response.status_code)


def post_data_set():
    dhis2_remote_repository.post_data_set(json.dumps(build_data_set_request_body_as_dict()))


def post_data_element_values():
    bes_middleware_cores = BesMiddlewareCore.objects.all()
    for bes_middleware_core in bes_middleware_cores:
        if bes_middleware_cores.last_update_date > SyncRecord.get_last_successful_sync_time():
            dhis2_remote_repository.post_data_elements_value(
                json.dumps(build_data_element_values_request_body_as_dict(bes_middleware_core)))


def build_data_element_values_request_body_as_dict(bes_middleware_core):
    elements = Element.objects.all()
    data_values = []
    for element in elements:
        data_values.append({
            'dataElement': element.id,
            'value': getattr(bes_middleware_core, element.name)
        })

    now = datetime.now()
    return {
        'dataSet': dhis2_config.DATA_SET_ID,
        'completeData': str(now),
        'period': str(now.strftime('%Y%m')),
        'orgUnit': Facility.objects.get(device_serial=bes_middleware_core.device_id).uid,
        'dataValues': data_values
    }


def build_data_set_request_body_as_dict():
    facilities = Facility.objects.all()
    elements = Element.objects.all()
    facility_ids_list = []
    element_ids_list = []
    for facility in facilities:
        facility_ids_list.append({'id': facility.uid})
    for element in elements:
        element_ids_list.append({'id': element.id})
    return {
        'dataElements': element_ids_list,
        'expiryDays': 0,
        'fieldCombinationRequired': False,
        'indicators': [],
        'mobile': False,
        'name': dhis2_config.DATA_SET_NAME,
        'openFuturePeriods': 0,
        'organisationUnits': facility_ids_list,
        'periodType': dhis2_config.DATA_SET_PERIOD_TYPES,
        'shortName': dhis2_config.DATA_SET_NAME,
        'timelyDays': 15
    }


def convert_attribute_to_dict(attribute):
    attr_type = attribute.attr_type + "Attribute"
    return {
        'id': attribute.uid,
        'code': attribute.code,
        'valueType': attribute.value_type,
        attr_type: True,
        'name': attribute.name
    }
