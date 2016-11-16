import logging
from xml.etree import ElementTree

from model_utils import Choices

from dsd.repositories import dhis2_remote_repository

logger = logging.getLogger(__name__)

PERIOD_TYPE = Choices('Weekly')
IMPORTANCE = Choices("HIGH", "MEDIUM", "LOW")
RULE_TYPE = Choices("VALIDATION", "SURVEILLANCE")
MISSING_VALUE_STRATEGY = Choices(
    'NEVER_SKIP',
    'SKIP_IF_ANY_VALUE_MISSING'
)

ADDITIONAL_RULE_TYPE = Choices(
    'Default',
    'MalariaCaseInYears',
    'DisenteriaCaseInYears',
    'MeningiteIncreasedInWeeks',
    'SarampoCaseInMonths'
)

OPERATOR = Choices(
    "equal_to",
    "not_equal_to",
    "greater_than",
    "greater_than_or_equal_to",
    "less_than",
    "less_than_or_equal_to",
    "compulsory_pair",
    "exclusive_pair"
)

ORGANISATION_UNIT_LEVEL = {
    'moh': 1,
    'province': 2,
    'district': 3,
    'facility': 4
}


def generate_validation_rule_xml(rule_id, rule_name, rule_description, rule_instruction, rule_type, period_type,
                                 importance, operator, organisation_unit_level, left_side_expression,
                                 left_side_description, date_element_ids, right_side_expression, right_side_description,
                                 additional_rule_type, additional_rule):
    name_space = 'http://dhis2.org/schema/dxf/2.0'
    root = ElementTree.Element('{%s}meteData' % name_space, nsmap={None: name_space})
    validation_rules = ElementTree.SubElement(root, 'validationRules')
    validation_rule = ElementTree.SubElement(validation_rules, 'validationRule')
    ElementTree.SubElement(validation_rule, 'id').text = rule_id
    ElementTree.SubElement(validation_rule, 'name').text = rule_name
    ElementTree.SubElement(validation_rule, 'description').text = rule_description
    ElementTree.SubElement(validation_rule, 'instruction').text = rule_instruction
    ElementTree.SubElement(validation_rule, 'ruleType').text = rule_type
    ElementTree.SubElement(validation_rule, 'periodType').text = period_type
    ElementTree.SubElement(validation_rule, 'importance').text = importance
    ElementTree.SubElement(validation_rule,
                           'additionalRuleType').text = additional_rule_type if additional_rule_type else None
    ElementTree.SubElement(validation_rule, 'additionalRule').text = additional_rule if additional_rule else None
    ElementTree.SubElement(validation_rule, 'operator').text = operator
    ElementTree.SubElement(validation_rule, 'organisationUnitLevel').text = organisation_unit_level

    left_side = ElementTree.SubElement(validation_rule, 'leftSide')
    ElementTree.SubElement(left_side, 'expression').text = left_side_expression
    ElementTree.SubElement(left_side, 'description').text = left_side_description
    ElementTree.SubElement(left_side, 'missingValueStrategy').text = MISSING_VALUE_STRATEGY.NEVER_SKIP
    ElementTree.SubElement(left_side, 'nullIfBlank').text = str(True).lower()
    date_elements = ElementTree.SubElement(left_side, 'dataElements')

    for date_element_id in date_element_ids:
        ElementTree.SubElement(date_elements, 'dataElement', id=date_element_id)

    right_side = ElementTree.SubElement(validation_rule, 'rightSide')
    ElementTree.SubElement(right_side, 'expression').text = right_side_expression
    ElementTree.SubElement(right_side, 'description').text = right_side_description
    ElementTree.SubElement(right_side, 'missingValueStrategy').text = MISSING_VALUE_STRATEGY.NEVER_SKIP
    ElementTree.SubElement(right_side, 'nullIfBlank').text = str(True).lower()
    return root


def generate_validation_rule_group_xml(group_id, name, description, validation_rule_id):
    name_space = 'http://dhis2.org/schema/dxf/2.0'
    root = ElementTree.Element('{%s}meteData' % name_space, nsmap={None: name_space})
    validation_rule_groups = ElementTree.SubElement(root, 'validationRuleGroups')
    validation_rule_group = ElementTree.SubElement(validation_rule_groups, 'validationRuleGroup')
    ElementTree.SubElement(validation_rule_group, 'id').text = group_id
    ElementTree.SubElement(validation_rule_group, 'name').text = name
    ElementTree.SubElement(validation_rule_group, 'description').text = description
    ElementTree.SubElement(validation_rule_group, 'alertByOrgUnits').text = str(True).lower()
    validation_rules = ElementTree.SubElement(validation_rule_group, 'validationRules')
    validation_rule = ElementTree.SubElement(validation_rules, 'validationRule')
    ElementTree.SubElement(validation_rule, 'id').text = validation_rule_id
    return root


def post_validation_rule(rule_id, rule_name, rule_description, rule_instruction, left_side_expression,
                         left_side_description, date_element_ids, right_side_expression, right_side_description='limite'
                         , organisation_unit_level=str(ORGANISATION_UNIT_LEVEL.get('facility')),
                         rule_type=RULE_TYPE.SURVEILLANCE, period_type=PERIOD_TYPE.Weekly, importance=IMPORTANCE.HIGH,
                         operator=OPERATOR.less_than_or_equal_to, additional_rule_type=ADDITIONAL_RULE_TYPE.Default,
                         additional_rule=None):
    doc = generate_validation_rule_xml(rule_id=rule_id,
                                       rule_name=rule_name,
                                       rule_description=rule_description,
                                       rule_instruction=rule_instruction,
                                       rule_type=rule_type,
                                       period_type=period_type,
                                       importance=importance,
                                       operator=operator,
                                       organisation_unit_level=organisation_unit_level,
                                       left_side_expression=left_side_expression,
                                       left_side_description=left_side_description,
                                       date_element_ids=date_element_ids,
                                       right_side_expression=right_side_expression,
                                       right_side_description=right_side_description,
                                       additional_rule_type=additional_rule_type,
                                       additional_rule=additional_rule)

    request_body = ElementTree.tostring(doc, encoding='utf8')
    logger.info(request_body)
    return dhis2_remote_repository.post_metadata(request_body)


def post_validation_rule_group(group_id, name, validation_rule_id, description=''):
    doc = generate_validation_rule_group_xml(group_id=group_id, name=name, description=description,
                                             validation_rule_id=validation_rule_id)

    return dhis2_remote_repository.post_metadata(ElementTree.tostring(doc))
