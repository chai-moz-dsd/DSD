import logging

from django.test import TestCase

from dsd.services.validation_rule_service import generate_validation_rule_xml, RULE_TYPE, IMPORTANCE, OPERATOR, \
    ORGANISATION_UNIT_LEVEL, PERIOD_TYPE, MISSING_VALUE_STRATEGY, generate_validation_rule_group_xml, \
    ADDITIONAL_RULE_TYPE

logger = logging.getLogger(__name__)


class ValidationRuleServiceTest(TestCase):
    def test_should_generate_validation_rule_group_xml(self):
        group_id = 'rf047709917'
        name = 'Cólera Casos Group'
        description = 'Threshold around Colera casos group'
        validation_rule_id = 'KtRVbWqZqNU'
        result = generate_validation_rule_group_xml(group_id=group_id, name=name, description=description,
                                                    validation_rule_id=validation_rule_id)
        validation_rule_group = result.find('validationRuleGroups/validationRuleGroup')
        self.assertEqual(validation_rule_group.find('id').text, group_id)
        self.assertEqual(validation_rule_group.find('name').text, name)
        self.assertEqual(validation_rule_group.find('description').text, description)
        self.assertEqual(validation_rule_group.find('validationRules/validationRule/id').text, validation_rule_id)

    def test_should_generate_validation_rule_xml(self):
        rule_id = 'KtRVbWqZqNU'
        rule_name = 'Cólera Casos'
        rule_description = 'Threshold around Colera casos'
        rule_instruction = 'Follow instructions around Colera outbreak'
        rule_type = RULE_TYPE.SURVEILLANCE,
        period_type = PERIOD_TYPE.Weekly
        importance = IMPORTANCE.HIGH
        operator = OPERATOR.less_than_or_equal_to
        organisation_unit_level = ORGANISATION_UNIT_LEVEL.get('facility')
        left_side_expression = '#{rf040c9a7ab.NwREtdtBRUN}'
        left_side_description = 'Cólera caso'
        date_element_ids = ['rf040c9a7ab', 'rf040c9a7ac']
        right_side_expression = '0'
        right_side_description = 'limite'
        additional_rule_type = ADDITIONAL_RULE_TYPE.Default
        addition_rule = None

        result = generate_validation_rule_xml(rule_id=rule_id,
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
                                              additional_rule=addition_rule)
        validation_rule = result.find('validationRules/validationRule')
        self.assertEqual(validation_rule.find('id').text, rule_id)
        self.assertEqual(validation_rule.find('name').text, rule_name)
        self.assertEqual(validation_rule.find('description').text, rule_description)
        self.assertEqual(validation_rule.find('instruction').text, rule_instruction)
        self.assertEqual(validation_rule.find('ruleType').text, rule_type)
        self.assertEqual(validation_rule.find('periodType').text, period_type)
        self.assertEqual(validation_rule.find('importance').text, importance)
        self.assertEqual(validation_rule.find('operator').text, operator)
        self.assertEqual(validation_rule.find('organisationUnitLevel').text, organisation_unit_level)

        left_side = validation_rule.find('leftSide')
        self.assertEqual(left_side.find('expression').text, left_side_expression)
        self.assertEqual(left_side.find('description').text, left_side_description)
        self.assertEqual(left_side.find('missingValueStrategy').text, MISSING_VALUE_STRATEGY.NEVER_SKIP)
        self.assertEqual(left_side.find('nullIfBlank').text, str(True).lower())

        date_elements = left_side.findall('dataElements/dataElement')
        self.assertEqual(date_elements[0].attrib.get('id'), date_element_ids[0])
        self.assertEqual(date_elements[1].attrib.get('id'), date_element_ids[1])

        right_side = validation_rule.find('rightSide')
        self.assertEqual(right_side.find('expression').text, right_side_expression)
        self.assertEqual(right_side.find('description').text, right_side_description)
        self.assertEqual(right_side.find('missingValueStrategy').text, MISSING_VALUE_STRATEGY.NEVER_SKIP)
        self.assertEqual(right_side.find('nullIfBlank').text, str(True).lower())
