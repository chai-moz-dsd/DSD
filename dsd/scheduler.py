import json
import logging

from dsd.config import dhis2_config
from dsd.models import Attribute
from dsd.models import Element
from dsd.models import SyncRecord
from dsd.models.moh import MoH
from dsd.repositories import dhis2_remote_repository
from dsd.repositories.dhis2_remote_repository import add_attribute, add_organization_unit, add_element
from dsd.repositories.request_template.add_attribute_template import AddAttributeRequestTemplate
from dsd.repositories.request_template.add_element_template import AddElementRequestTemplate
from dsd.services import bes_middleware_core_service
from dsd.services import district_service
from dsd.services import facility_service
from dsd.services import province_service
from dsd.services import sender_middleware_core_service
from dsd.services.bes_middleware_core_service import build_data_set_request_body_as_dict

logger = logging.getLogger(__name__)


def start():
    try:
        logger.info('Sync start...')
        sync_time = SyncRecord.get_last_successful_sync_time()

        sync_metadata()
        sync_data(sync_time)

        logger.info('Sync success!')
        SyncRecord.get_successful_instance().save()
    except Exception as e:
        logger.error('Sync error: %s!' % e)
        SyncRecord.get_fail_instance().save()

    post_data_set()


def sync_metadata():
    province_service.sync()
    district_service.sync()
    facility_service.sync()


def sync_data(sync_time):
    bes_middleware_core_service.sync(sync_time)
    sender_middleware_core_service.sync(sync_time)


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
                                                              name=element.name)
        response = add_element(json.dumps(request_body_dict))
        logger.info("response status = %s" % response.status_code)


def post_data_set():
    dhis2_remote_repository.post_data_set(json.dumps(build_data_set_request_body_as_dict()))
