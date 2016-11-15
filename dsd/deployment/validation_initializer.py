from dsd.models import Element
from dsd.services.data_value_validation_service import DataElementValuesValidationService
from dsd.services.validation_rule_service import ORGANISATION_UNIT_LEVEL, RULE_TYPE, IMPORTANCE, OPERATOR, \
    post_validation_rule, post_validation_rule_group


def add_colera():
    rule_id = 'tOCXddkXkw0'
    disease_code = '001_CÓLERA'
    date_element_id = Element.objects.get(code=disease_code).id

    assemble_left_side_expression(disease_code, 'cases_cholera')

    organisation_unit_level = ORGANISATION_UNIT_LEVEL.get('facility')
    left_side_expression = '#{rf040c9a7ab.NwREtdtBRUN}'

    post_validation_rule(rule_id=rule_id,
                         rule_name='Cólera Casos',
                         rule_description='Threshold around Colera casos',
                         rule_instruction='Follow instructions around Colera outbreak',
                         rule_type=RULE_TYPE.SURVEILLANCE,
                         period_type=IMPORTANCE.HIGH,
                         importance=OPERATOR.less_than_or_equal_to,
                         operator=ORGANISATION_UNIT_LEVEL.get('facility'),
                         organisation_unit_level=organisation_unit_level,
                         left_side_expression=left_side_expression,
                         left_side_description='Cólera caso',
                         date_element_id=date_element_id,
                         right_side_expression='0',
                         right_side_description='0')

    post_validation_rule_group(group_id='ahkz0JjYY3U', name='Cólera grupo', description='',
                               validation_rule_id=rule_id)


def assemble_left_side_expression(disease_code, query_name_prefix):
    element_ids = DataElementValuesValidationService.get_element_ids(disease_code=disease_code,
                                                                     query_name_prefix=query_name_prefix)
    expression_units = ['#{%s}' % element_id for element_id in element_ids]
    return '+'.join(expression_units)
