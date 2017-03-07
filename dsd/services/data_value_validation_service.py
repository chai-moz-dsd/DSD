import datetime
import json
import logging
from statistics import mean, stdev

import re
from django.db.models import Q
from rest_framework.status import HTTP_200_OK

from dsd.config.dhis2_config import DISEASE_I18N_MAP, THREE_WEEKS_DAYS, \
    CUSTOMIZED_VALIDATION_RULE_TYPE_PARAMS_REGEX, \
    CUSTOMIZED_VALIDATION_RULE_TYPE_PARAMS_REPLACEMENT, CUSTOMIZED_VALIDATION_RULE_TYPE_PARAMS, MEASLES_CASES, \
    CUSTOMIZED_VALIDATION_RULE_TYPE, MENINGITIS_CASES, MALARIA_CASES, DYSENTERY_CASES, ONE_WEEK_DAYS
from dsd.models import COCRelation
from dsd.models import Element
from dsd.models import Facility
from dsd.models.moh import MOH_UID
from dsd.repositories import dhis2_remote_repository
from dsd.services.alert_service import should_send_alert, update_alert_status
from dsd.services.dhis2_remote_service import construct_get_element_values_request_query_params

logger = logging.getLogger(__name__)

logger.setLevel(logging.CRITICAL)

FETCH_CUSTOMIZED_VALIDATION_RULES_REQUEST_PARAMS = 'fields=id' \
                                                   '&fields=validationRuleGroups' \
                                                   '&fields=additionalRuleType' \
                                                   '&fields=additionalRule' \
                                                   '&filter=additionalRuleType:ne:Default'

FETCH_DEFAULT_VALIDATION_RULES_REQUEST_PARAMS = 'fields=id' \
                                                '&fields=validationRuleGroups' \
                                                '&fields=organisationUnitLevel' \
                                                '&filter=additionalRuleType:eq:Default'

DATA_VALUE_INDEX = 2

MOH_LEVEL = 1
PROVINCE_LEVEL = 2
DISTRICT_LEVEL = 3
FACILITY_LEVEL = 4


def calculate_values_by_rows_data(rows):
    values = sum(map(lambda x: int(float(x[DATA_VALUE_INDEX])), rows))
    return values


def get_district_id(facility_id):
    facility = Facility.objects.filter(uid=facility_id).first()
    return facility.district.uid


def get_province_id(facility_id):
    facility = Facility.objects.filter(uid=facility_id).first()
    return facility.province.uid


ORGANISATION_UNIT_LEVEL_FUNC = {
    MOH_LEVEL: lambda x: MOH_UID,
    PROVINCE_LEVEL: get_province_id,
    DISTRICT_LEVEL: get_district_id,
    FACILITY_LEVEL: lambda x: x,
}


def get_matched_org_id_by_rule(facility_id, level):
    org_func = ORGANISATION_UNIT_LEVEL_FUNC.get(level)
    return org_func(facility_id)


def fetch_malaria_in_previous_weeks(year, week_num, week_offset, organisation_id):
    period_weeks = ['%sW%s' % (DataElementValuesValidationService.calculate_year_week_by_offset(year, week_num, i))
                    for i in range(-week_offset, 1)]

    return fetch_malaria_by_year_weeks(period_weeks, organisation_id)


def fetch_same_period_in_recent_years(current_year, year_offset, week_num, weeks_before, weeks_after,
                                      organisation_id):
    five_years_malaria = []
    for year in range(current_year - year_offset, current_year):
        malaria = fetch_malaria_by_year_and_weeks_range('%s' % year,
                                                        week_num, weeks_before,
                                                        weeks_after,
                                                        organisation_id)
        five_years_malaria.append(malaria)

    return five_years_malaria


def fetch_malaria_by_year_weeks(period_weeks, organisation_id):
    confirmed_ids = DataElementValuesValidationService.get_element_ids(disease_code='MALARIA_CONFIRMADA',
                                                                       query_name_prefix='cases_malaria')
    clinic_ids = DataElementValuesValidationService.get_element_ids(disease_code='MALARIA_CLINICA',
                                                                    query_name_prefix='cases_malaria')

    return DataElementValuesValidationService.fetch_disease_in_year_weeks(organisation_id,
                                                                          confirmed_ids + clinic_ids,
                                                                          period_weeks)


def fetch_malaria_by_year_and_weeks_range(year, week_num, weeks_before, after_weeks, organisation_id):
    period_weeks = ['%sW%s' % (DataElementValuesValidationService.calculate_year_week_by_offset(year, week_num, i))
                    for i in range(-weeks_before, after_weeks + 1)]

    return fetch_malaria_by_year_weeks(period_weeks, organisation_id)


class DataElementValuesValidationService(object):
    def __init__(self):
        _, self.rule_group_name_id_map = self.fetch_all_rule_groups()
        customized_rule_type_to_addition_rules, self.customized_rule_type_to_rule_ids, self.customized_rule_type_to_rule_groups = self.fetch_customized_validation_rules()
        self.customized_rule_type_to_addition_rules = self.extract_params_from_customize_rules(
            customized_rule_type_to_addition_rules)

    def validate_values(self, date_element_values):
        for value in date_element_values:
            try:
                facility = Facility.objects.get(id=value.middleware_facility_id)
                if not facility:
                    continue
                organization_id = facility.uid
                self.send_validation_for_each_disease(value, organization_id)
                self.send_validation_for_sarampo_in_recent_weeks(value, organization_id)
                self.send_validation_for_meningitis_every_two_weeks(value, organization_id)
                self.send_validation_malaria_in_recent_years_average(value, organization_id)
                self.send_validation_dysentery_recent_years_average(value, organization_id)
            except Exception as e:
                logger.error('validate_values error : %s!' % e)

    @staticmethod
    def week_range_in_updated_data(value):
        year = value.bes_year.year
        week_time = '%s-W%s' % (year, value.bes_number)

        date_week_start = datetime.datetime.strptime('%s-1' % week_time, '%Y-W%W-%w').strftime('%Y-%m-%d')
        date_week_end = datetime.datetime.strptime('%s-0' % week_time, '%Y-W%W-%w').strftime('%Y-%m-%d')

        return date_week_start, date_week_end

    @staticmethod
    def format_validation_request_url(organisation_id, start_date, end_date, rule_group_id, alert_should_be_sent):
        alert_flag = 'true' if alert_should_be_sent else 'false'
        validate_params = 'organisationUnitId=%s&startDate=%s&endDate=%s&validationRuleGroupId=%s&sendAlerts=%s' % \
                          (organisation_id,
                           start_date,
                           end_date,
                           rule_group_id,
                           alert_flag)
        return validate_params

    @staticmethod
    def fetch_validation_rule_groups_from_html(html_text):
        validation_rule_groups = {}
        validation_rule_group_pattern = re.compile(r'<tr\sid="tr(\d+)".+data-name="(.+)"')

        for line in html_text.split('\n'):
            ma = re.search(validation_rule_group_pattern, line)
            if ma:
                validation_rule_groups.setdefault(ma.group(2), ma.group(1))

        return validation_rule_groups

    @staticmethod
    def change_date_to_days_before(current_date, the_days_before):
        current_date_format = datetime.datetime.strptime(current_date, '%Y-%m-%d')
        before_date = current_date_format - datetime.timedelta(days=the_days_before)
        return before_date.strftime("%Y-%m-%d")

    def fetch_all_rule_groups(self):
        response = dhis2_remote_repository.get_all_rule_groups()
        return response.status_code, self.fetch_validation_rule_groups_from_html(response.text)

    def get_rule_group_id(self, element_name):
        return self.rule_group_name_id_map.get('%s GROUP' % DISEASE_I18N_MAP.get(element_name))

    def send_validation_request_to_dhis2(self, date_week_start, date_week_end,
                                         rule_group_id, validated_org_id):
        should_alert = should_send_alert(rule_group_id, validated_org_id)
        logger.debug('should alert: {} rule_group_id: {} validated_organisation_id: {}'.format(should_alert,
                                                                                               rule_group_id,
                                                                                               validated_org_id))
        return self.send_validation_request(rule_group_id,
                                            date_week_start,
                                            date_week_end,
                                            validated_org_id,
                                            should_alert)

    def send_validation_for_each_disease(self, value, organisation_id):
        date_week_start, date_week_end = self.week_range_in_updated_data(value)

        for rule_id, rule_info in self.fetch_default_validation_rules().items():
            rule_group_id, rule_org_unit_level = rule_info
            validated_org_id = get_matched_org_id_by_rule(organisation_id, rule_org_unit_level)
            logger.debug(
                'each: middleware_facility_id = %s, rule_id = %s: rule_group_id = %s, start = %s, end = %s ' % (
                    value.middleware_facility_id, rule_id, rule_group_id, date_week_start, date_week_end))

            response = self.send_validation_request_to_dhis2(date_week_start,
                                                             date_week_end,
                                                             rule_group_id,
                                                             validated_org_id)

            if response.status_code != HTTP_200_OK:
                logger.error('validate request failed, response = %s' % response)
                return

            update_alert_status(rule_group_id, validated_org_id, self.__should_alert_next_time(response))

    @staticmethod
    def __should_alert_next_time(response):
        return ('Validation passed successfully' in response.text) or ('Validado com sucesso' in response.text)

    @staticmethod
    def send_validation_request(rule_group_id, start_date, end_date, organisation_id, should_alert):
        validate_params = DataElementValuesValidationService.format_validation_request_url(organisation_id, start_date,
                                                                                           end_date, rule_group_id,
                                                                                           should_alert)
        if should_alert:
            logger.debug('validate_params = %s' % validate_params)
        return dhis2_remote_repository.get_validation_results(validate_params)

    def send_validation_malaria_in_recent_years_average(self, value, organisation_id):
        rule_type = CUSTOMIZED_VALIDATION_RULE_TYPE.get(MALARIA_CASES)
        weeks_before = self.customized_rule_type_to_addition_rules.get(rule_type).get('weeks_before')
        weeks_after = self.customized_rule_type_to_addition_rules.get(rule_type).get('weeks_after')

        _, data_week_end = self.week_range_in_updated_data(value)
        data_week_start = self.change_date_to_days_before(data_week_end,
                                                          (weeks_before + weeks_after + 1) * ONE_WEEK_DAYS - 1)

        rule_group_id = self.customized_rule_type_to_rule_groups.get(CUSTOMIZED_VALIDATION_RULE_TYPE.get(MALARIA_CASES))
        validated_org_id = get_matched_org_id_by_rule(organisation_id, FACILITY_LEVEL)

        if self.matched_malaria_customized_rule(organisation_id, rule_type, value, weeks_after, weeks_before):
            response = self.send_validation_request_to_dhis2(data_week_start,
                                                             data_week_end,
                                                             rule_group_id,
                                                             validated_org_id)

            if response.status_code != HTTP_200_OK:
                logger.error('validate request failed, response = %s' % response)
                return

            update_alert_status(rule_group_id, validated_org_id, self.__should_alert_next_time(response))
        else:
            update_alert_status(rule_group_id, validated_org_id, True)

    def matched_malaria_customized_rule(self, organisation_id, rule_type, value, weeks_after, weeks_before):
        current_year = value.bes_year.year
        week_num = value.bes_number
        recent_years = self.customized_rule_type_to_addition_rules.get(rule_type).get('recent_years')
        std_dev_factor = self.customized_rule_type_to_addition_rules.get(rule_type).get('std_dev')

        reporting_period_cases = fetch_malaria_in_previous_weeks(current_year,
                                                                 week_num,
                                                                 weeks_before + weeks_after,
                                                                 organisation_id)

        recent_years_cases = fetch_same_period_in_recent_years(current_year,
                                                               recent_years,
                                                               week_num,
                                                               weeks_before,
                                                               weeks_after,
                                                               organisation_id)
        average_cases_in_recent_years = mean(recent_years_cases)
        std_dev_cases_in_recent_years = stdev(recent_years_cases)

        logger.debug('customized malaria rule: reporting_period_cases = {}, average_cases_in_recent_years = {}'
                     'std_dev_cases_in_recent_years = {}'.format(reporting_period_cases,
                                                                 average_cases_in_recent_years,
                                                                 std_dev_cases_in_recent_years))

        return reporting_period_cases > average_cases_in_recent_years + std_dev_factor * std_dev_cases_in_recent_years

    def send_validation_dysentery_recent_years_average(self, value, organisation_id):
        current_year = value.bes_year.year
        week_num = value.bes_number
        recent_years = self.customized_rule_type_to_addition_rules.get(
            CUSTOMIZED_VALIDATION_RULE_TYPE.get(DYSENTERY_CASES)).get(
            'recent_years')
        std_dev = self.customized_rule_type_to_addition_rules.get(
            CUSTOMIZED_VALIDATION_RULE_TYPE.get(DYSENTERY_CASES)).get(
            'std_dev')

        dysentery_in_current_week = self.fetch_dysentery_in_week_num(current_year, week_num, organisation_id)
        dysentery_five_years_same_week = self.fetch_dysentery_same_week_in_recent_five_years(current_year, recent_years,
                                                                                             week_num, organisation_id)

        average_five_years_dysentery = mean(dysentery_five_years_same_week)
        std_dev_five_years_dysentery = stdev(dysentery_five_years_same_week)

        data_week_start, data_week_end = self.week_range_in_updated_data(value)
        rule_group_id = self.customized_rule_type_to_rule_groups.get(
            CUSTOMIZED_VALIDATION_RULE_TYPE.get(DYSENTERY_CASES))
        validated_org_id = get_matched_org_id_by_rule(organisation_id, FACILITY_LEVEL)
        if dysentery_in_current_week > average_five_years_dysentery + std_dev * std_dev_five_years_dysentery:
            logger.debug(
                'dysentery: rule_group_id = %s, start=%s, end=%s, average_five_years=%s, std_dev_five_years=%s' % (
                    rule_group_id, data_week_start, data_week_end, average_five_years_dysentery,
                    std_dev_five_years_dysentery))

            response = self.send_validation_request_to_dhis2(data_week_start,
                                                             data_week_end,
                                                             rule_group_id,
                                                             validated_org_id)

            if response.status_code != HTTP_200_OK:
                logger.error('validate request failed, response = %s' % response)
                return

            update_alert_status(rule_group_id, validated_org_id, self.__should_alert_next_time(response))
        else:
            update_alert_status(rule_group_id, validated_org_id, True)

    def send_validation_for_sarampo_in_recent_weeks(self, value, organisation_id):
        current_year = value.bes_year.year
        week_num = value.bes_number
        start, data_week_end = self.week_range_in_updated_data(value)

        week_offset = self.customized_rule_type_to_addition_rules.get(
            CUSTOMIZED_VALIDATION_RULE_TYPE.get(MEASLES_CASES)).get(
            'recent_weeks')
        threshold = self.customized_rule_type_to_addition_rules.get(
            CUSTOMIZED_VALIDATION_RULE_TYPE.get(MEASLES_CASES)).get(
            'threshold')

        sarampo_cases_in_a_month = self.fetch_sarampo_by_period(current_year, week_num, week_offset, organisation_id)
        logger.debug('sarampo_cases_in_a_month values: %d threshold: %d' % (sarampo_cases_in_a_month, threshold))

        rule_group_id = self.customized_rule_type_to_rule_groups.get(CUSTOMIZED_VALIDATION_RULE_TYPE.get(MEASLES_CASES))
        validated_org_id = get_matched_org_id_by_rule(organisation_id, DISTRICT_LEVEL)
        if sarampo_cases_in_a_month > threshold:
            data_week_start = self.change_date_to_days_before(start, THREE_WEEKS_DAYS)

            logger.debug('sarampo: rule_group_id = %s, start=%s, end=%s, cases_in_a_month=%s' % (
                rule_group_id, data_week_start, data_week_end, sarampo_cases_in_a_month))

            response = self.send_validation_request_to_dhis2(data_week_start,
                                                             data_week_end,
                                                             rule_group_id,
                                                             validated_org_id)

            if response.status_code != HTTP_200_OK:
                logger.error('validate request failed, response = %s' % response)
                return

            update_alert_status(rule_group_id, validated_org_id, self.__should_alert_next_time(response))
        else:
            update_alert_status(rule_group_id, validated_org_id, True)

    def send_validation_for_meningitis_every_two_weeks(self, value, organisation_id):
        current_year = value.bes_year.year
        week_num = value.bes_number

        recent_weeks = self.customized_rule_type_to_addition_rules.get(
            CUSTOMIZED_VALIDATION_RULE_TYPE.get(MENINGITIS_CASES)).get(
            'recent_weeks')
        increased_times = self.customized_rule_type_to_addition_rules.get(
            CUSTOMIZED_VALIDATION_RULE_TYPE.get(MENINGITIS_CASES)).get('times')

        is_rule_matched = self.is_meningitis_increasement_rule_match(current_year, week_num, organisation_id,
                                                                     increased_times,
                                                                     recent_weeks)

        rule_group_id = self.customized_rule_type_to_rule_groups.get(
            CUSTOMIZED_VALIDATION_RULE_TYPE.get(MENINGITIS_CASES))
        validated_org_id = get_matched_org_id_by_rule(organisation_id, FACILITY_LEVEL)
        if is_rule_matched:
            _, data_week_end = self.week_range_in_updated_data(value)
            data_week_start = self.change_date_to_days_before(data_week_end, THREE_WEEKS_DAYS)

            response = self.send_validation_request_to_dhis2(data_week_start,
                                                             data_week_end,
                                                             rule_group_id,
                                                             validated_org_id)

            if response.status_code != HTTP_200_OK:
                logger.error('validate request failed, response = %s' % response)
                return

            update_alert_status(rule_group_id, validated_org_id, self.__should_alert_next_time(response))
        else:
            update_alert_status(rule_group_id, validated_org_id, True)

    @staticmethod
    def is_meningitis_increasement_rule_match(year, week, organisation_id, increased_times, week_offset):
        current_year, current_week = DataElementValuesValidationService.calculate_year_week_by_offset(year, week, 0)

        meningitis_cases_current_week = DataElementValuesValidationService.fetch_meningitis(current_year,
                                                                                            current_week,
                                                                                            organisation_id)
        logger.debug('year = %s,week=%s' % (year, week))
        for offset in range(0, -week_offset + 1, -1):
            previous_year, previous_week = DataElementValuesValidationService.calculate_year_week_by_offset(year, week,
                                                                                                            offset - 1)
            meningitis_cases_previous_week = DataElementValuesValidationService.fetch_meningitis(previous_year,
                                                                                                 previous_week,
                                                                                                 organisation_id)
            logger.debug('meningitis: cases_current_week = %s,cases_previous_week=%s' % (
                meningitis_cases_current_week, meningitis_cases_previous_week))
            if meningitis_cases_previous_week == 0 or meningitis_cases_current_week < meningitis_cases_previous_week * increased_times:
                logger.debug('meningitis : ********Don not match******')
                return False
            meningitis_cases_current_week = meningitis_cases_previous_week

        return True

    @staticmethod
    def calculate_year_week_by_offset(current_year, current_week, offset_weeks):
        current_week_start_date = datetime.datetime.strptime('%s-W%s-0' % (current_year, current_week), '%Y-W%U-%w')
        target_week_start_date = current_week_start_date + datetime.timedelta(weeks=offset_weeks)
        return int(target_week_start_date.strftime('%Y')), int(target_week_start_date.strftime('%U'))

    @staticmethod
    def fetch_meningitis(year, week_num, organisation_id):
        period_weeks = ['%sW%s' % (year, week_num)]
        element_ids = DataElementValuesValidationService.get_element_ids(disease_code='MENINGITE_036',
                                                                         query_name_prefix='cases_meningitis')
        return DataElementValuesValidationService.fetch_disease_in_year_weeks(organisation_id, element_ids,
                                                                              period_weeks)

    @staticmethod
    def fetch_sarampo_by_period(year, week_num, week_offset, organisation_id):
        period_weeks = ['%sW%s' % (DataElementValuesValidationService.calculate_year_week_by_offset(year, week_num, i))
                        for i in range(-week_offset + 1, 1)]

        element_ids = DataElementValuesValidationService.get_element_ids(disease_code='SARAMPO_055',
                                                                         query_name_prefix='cases_measles')
        special_element_ids = DataElementValuesValidationService.get_element_ids(disease_code='SARAMPO_055',
                                                                                 query_name_prefix='cases_nv_measles')

        element_ids.extend(special_element_ids)
        return DataElementValuesValidationService.fetch_disease_in_year_weeks(organisation_id, element_ids,
                                                                              period_weeks)

    @staticmethod
    def fetch_dysentery_in_week_num(current_year, week_num, organisation_id):
        period_weeks = ['%sW%s' % (current_year, week_num)]
        element_ids = DataElementValuesValidationService.get_element_ids(disease_code='009.2_DISENTERIA',
                                                                         query_name_prefix='cases_dysentery')
        return DataElementValuesValidationService.fetch_disease_in_year_weeks(organisation_id, element_ids,
                                                                              period_weeks)

    @staticmethod
    def fetch_disease_in_year_weeks(organisation_id, element_ids, period_weeks):
        query_params = construct_get_element_values_request_query_params(
            organisation_unit_id=organisation_id,
            element_ids=element_ids,
            period_weeks=period_weeks
        )
        element_data = dhis2_remote_repository.get_data_element_values(query_params).json().get('rows')
        return calculate_values_by_rows_data(element_data)

    @staticmethod
    def get_element_ids(disease_code, query_name_prefix):
        result = []
        element_id = Element.objects.filter(code=disease_code).first().id
        for coc in COCRelation.objects.filter(Q(name_in_bes__startswith=query_name_prefix), Q(element_id=element_id)):
            result.append('%s.%s' % (element_id, coc.coc_id))
        return result

    @staticmethod
    def assemble_left_side_expression(disease_code, query_name_prefix):
        element_ids = DataElementValuesValidationService.get_element_ids(disease_code=disease_code,
                                                                         query_name_prefix=query_name_prefix)
        expression_units = ['#{%s}' % element_id for element_id in element_ids]
        return '+'.join(expression_units)

    @staticmethod
    def fetch_dysentery_same_week_in_recent_five_years(current_year, year_offset, week_num, organisation_id):
        five_years_diarrhea = []

        for year in range(current_year - year_offset, current_year):
            diarrhea = DataElementValuesValidationService.fetch_dysentery_in_week_num('%s' % year, week_num,
                                                                                      organisation_id)
            five_years_diarrhea.append(diarrhea)
        return five_years_diarrhea

    @staticmethod
    def extract_params_from_customize_rules(rule_type_to_addition_rules):
        result = {}
        for rule_type, rule in rule_type_to_addition_rules.items():
            result.update({rule_type: DataElementValuesValidationService.parse_rule_params(rule_type, rule)})
        return result

    @staticmethod
    def fetch_customized_validation_rules():
        rule_type_to_addition_rules = {}
        rule_type_to_rules_ids = {}
        rule_type_to_rule_groups = {}
        response = dhis2_remote_repository.get_validation_rules(FETCH_CUSTOMIZED_VALIDATION_RULES_REQUEST_PARAMS)
        logger.debug('response =%s' % response)
        response_json = response.json()
        for rule in response_json.get('validationRules'):
            rule_type_to_addition_rules.update({rule.get('additionalRuleType'): rule.get('additionalRule')})
            rule_type_to_rules_ids.update({rule.get('additionalRuleType'): rule.get('id')})
            validationRuleGroups = rule.get('validationRuleGroups')
            rule_type_to_rule_groups.update({rule.get('additionalRuleType'): validationRuleGroups[0].get('id')}) if len(
                validationRuleGroups) else None
        return rule_type_to_addition_rules, rule_type_to_rules_ids, rule_type_to_rule_groups

    @staticmethod
    def fetch_default_validation_rules():
        result = {}
        response = dhis2_remote_repository.get_validation_rules(FETCH_DEFAULT_VALIDATION_RULES_REQUEST_PARAMS)
        logger.debug('response =%s' % response)
        response_json = response.json()
        for rule in response_json.get('validationRules'):
            validationRuleGroups = rule.get('validationRuleGroups')
            rule_org_unit_level = rule.get('organisationUnitLevel')
            result.update({rule.get('id'): (validationRuleGroups[0].get('id'), rule_org_unit_level)}) if len(
                validationRuleGroups) > 0 else None
        return result

    @staticmethod
    def parse_rule_params(rule_type, rule):
        cleaned_rule = rule.replace('\r', '').replace('\n', '').replace(' ', '')
        rule_regex = CUSTOMIZED_VALIDATION_RULE_TYPE_PARAMS_REGEX.get(rule_type)
        rule_replacement = CUSTOMIZED_VALIDATION_RULE_TYPE_PARAMS_REPLACEMENT.get(rule_type)
        extracted_params = CUSTOMIZED_VALIDATION_RULE_TYPE_PARAMS.get(rule_type)
        result = {}
        params = json.loads(re.sub(rule_regex, rule_replacement, cleaned_rule))
        for key, value in extracted_params.items():
            result.update({key: params.get(value)})

        return result
