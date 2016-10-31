import datetime
import json
import logging

from dsd.config import dhis2_config
from dsd.models import Attribute
from dsd.models import COCRelation
from dsd.models import Category
from dsd.models import CategoryCombination
from dsd.models import CategoryOption
from dsd.models import District
from dsd.models import Element
from dsd.models import Facility
from dsd.models.moh import MoH, MOH_UID
from dsd.repositories import dhis2_remote_repository
from dsd.repositories.dhis2_remote_repository import post_attribute
from dsd.repositories.dhis2_remote_repository import post_element, post_organization_unit
from dsd.repositories.request_template.add_element_template import AddElementRequestTemplate

logger = logging.getLogger(__name__)


def post_attributes():
    logger.info('=== START SYNC ATTRIBUTES ===')
    attributes = Attribute.objects.all()
    for attribute in attributes:
        request_body_dict = convert_attribute_to_dict(attribute)
        logger.info(request_body_dict)
        response = post_attribute(json.dumps(request_body_dict))
        logger.info('response status = %s' % response.status_code)


def post_elements():
    logger.info('=== START SYNC DATA ELEMENTS ===')
    elements = Element.objects.all()
    for element in elements:
        request_body_dict = AddElementRequestTemplate().build(id=element.id,
                                                              code=element.code,
                                                              value_type=element.value_type,
                                                              short_name=element.short_name,
                                                              domain_type=element.domain_type,
                                                              category_combo=element.category_combo.id,
                                                              aggregation_type=element.aggregation_type,
                                                              name=element.name)
        response = post_element(json.dumps(request_body_dict))
        logger.info('response status = %s' % response)


def post_organization_units():
    logger.info('=== START SYNC ORGANIZATION UNITS ===')
    organization_units = MoH().get_organization_as_list()
    for organization_unit in organization_units:
        logger.info('response unit = %s' % organization_unit)
        response = post_organization_unit(json.dumps(organization_unit))
        logger.info('response status = %s' % response.status_code)


def get_user_profile():
    profile = dhis2_remote_repository.get_self_profile()
    profile_json = json.loads(profile)
    return profile_json.get('id'), profile_json.get('surname'), profile_json.get('firstName')


def assign_all_org_to_user():
    logger.info('assign_all_org_to_user')
    user_id, surname, first_name = get_user_profile()
    dhis2_remote_repository.update_user(json.dumps(user_update_body(surname, first_name)), user_id)


def set_org_unit_level():
    dhis2_remote_repository.post_to_set_org_level(json.dumps(build_org_level_dict()))


def post_category_options():
    logger.info('=== START SYNC CATEGORY OPTIONS ===')
    for category_option in CategoryOption.objects.all():
        request_body_dict = build_category_options_request_body_as_dict(category_option)
        dhis2_remote_repository.post_category_options(json.dumps(request_body_dict))


def post_categories():
    logger.info('=== START SYNC CATEGORIES ===')
    for category in Category.objects.all():
        request_body_dict = build_categories_request_body_as_dict(category)
        dhis2_remote_repository.post_categories(json.dumps(request_body_dict))


def post_category_combinations():
    logger.info('=== START SYNC CATEGORY COMBINATIONS ===')
    for category_combination in CategoryCombination.objects.all():
        request_body_dict = build_category_combinations_request_body_as_dict(category_combination)
        dhis2_remote_repository.post_category_combinations(json.dumps(request_body_dict))


def post_data_set():
    logger.info('=== START SYNC DATASET ===')
    dhis2_remote_repository.post_data_set(json.dumps(build_data_set_request_body_as_dict()))


def post_data_element_values(date_element_values):
    logger.info('=== START POSt DATA VALUE ===')
    for data_element in date_element_values:
        try:
            json_dumps = json.dumps(build_data_element_values_request_body_as_dict(data_element))
            dhis2_remote_repository.post_data_elements_value(json_dumps)
        except Exception as e:
            logger.error('post data element =%s, error occur =  %s' % (data_element, e))


def build_data_element_values_request_body_as_dict(bes_middleware_core):
    coc_relations = COCRelation.objects.all()
    data_values = []
    for coc_relation in coc_relations:
        value = getattr(bes_middleware_core, coc_relation.name_in_bes)
        if isinstance(value, int) and value >= 0:
            data_values.append({
                'dataElement': coc_relation.element_id,
                'value': value,
                'categoryOptionCombo': coc_relation.coc_id,
            })
    if bes_middleware_core.bes_year:
        year = bes_middleware_core.bes_year
    else:
        year = datetime.datetime.now()
    start_week = "%sW%s" % (str(year)[:4], str(bes_middleware_core.bes_number))
    return {
        'dataSet': dhis2_config.DATA_SET_ID,
        'completeData': str(bes_middleware_core.submission_date),
        'period': start_week,
        'orgUnit': Facility.objects.get(device_serial=bes_middleware_core.device_id).uid,
        'dataValues': data_values
    }


def build_data_set_request_body_as_dict():
    organisation_units = []
    element_ids_list = []
    for facility in Facility.objects.all():
        organisation_units.append({'id': facility.uid})
    for district in District.objects.all():
        organisation_units.append({'id': district.uid})
    for element in Element.objects.all():
        element_ids_list.append({'id': element.id})
    return {
        'dataElements': element_ids_list,
        'expiryDays': 0,
        'fieldCombinationRequired': False,
        'indicators': [],
        'mobile': False,
        'id': dhis2_config.DATA_SET_ID,
        'name': dhis2_config.DATA_SET_NAME,
        'openFuturePeriods': 0,
        'organisationUnits': organisation_units,
        'periodType': dhis2_config.DATA_SET_PERIOD_TYPES,
        'shortName': dhis2_config.DATA_SET_NAME,
        'timelyDays': 15
    }


def convert_attribute_to_dict(attribute):
    attr_type = '%sAttribute' % attribute.attr_type
    return {
        'id': attribute.uid,
        'code': attribute.code,
        'valueType': attribute.value_type,
        attr_type: True,
        'name': attribute.name
    }


def construct_get_element_values_request_query_params(organisation_unit_id, element_ids, period_weeks):
    query_params = 'dimension=dx:%s&dimension=ou:%s&filter=pe:%s' % (
        ';'.join(element_ids), organisation_unit_id, ';'.join(period_weeks))
    return '%s' % query_params


def build_category_options_request_body_as_dict(category_option):
    organisation_units = []
    for facility in Facility.objects.all():
        organisation_units.append({'id': facility.uid})
    for district in District.objects.all():
        organisation_units.append({'id': district.uid})
    return {
        'id': category_option.id,
        'name': category_option.name,
        'organisationUnits': organisation_units
    }


def build_categories_request_body_as_dict(category):
    category_options = []
    for category_option in CategoryOption.objects.filter(category=category):
        category_options.append({'id': category_option.id})

    return {
        'id': category.id,
        'name': category.name,
        'categoryOptions': category_options,
        'dataDimension': dhis2_config.CATEGORY_DATA_DIMENSION,
        'dataDimensionType': dhis2_config.CATEGORY_DATA_DIMENSION_TYPE
    }


def build_category_combinations_request_body_as_dict(category_combination):
    categories = []
    for category in Category.objects.filter(categorycombination=category_combination):
        categories.append({'id': category.id})

    return {
        'categories': categories,
        'id': category_combination.id,
        'name': category_combination.name,
        'dataDimensionType': dhis2_config.CATEGORY_DATA_DIMENSION_TYPE
    }


def user_update_body(surname, first_name):
    return {
        'surname': surname,
        'firstName': first_name,
        'organisationUnits': [{
            'id': MOH_UID
        }]
    }


def build_org_level_dict():
    return {'organisationUnitLevels':
        [
            {'name': 'MoH', 'level': 1, 'offlineLevels': 1},
            {'name': 'Province', 'level': 2, 'offlineLevels': 2},
            {'name': 'District', 'level': 3, 'offlineLevels': 3},
            {'name': 'Facility', 'level': 4, 'offlineLevels': 4}
        ]
    }
