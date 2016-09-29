import datetime
import json
import logging
import re
from statistics import mean, stdev

from rest_framework.status import HTTP_200_OK

from dsd.config.dhis2_config import DISEASE_I18N_MAP, THREE_WEEKS_DAYS, \
    CUSTOMIZED_VALIDATION_RULE_TYPE_PARAMS_REGEX, \
    CUSTOMIZED_VALIDATION_RULE_TYPE_PARAMS_REPLACEMENT, CUSTOMIZED_VALIDATION_RULE_TYPE_PARAMS, MEASLES_CASES, \
    CUSTOMIZED_VALIDATION_RULE_TYPE, MENINGITIS_CASES, MALARIA_CASES, DYSENTERY_CASES, ONE_WEEK_DAYS
from dsd.models import Element
from dsd.models.moh import MOH_UID
from dsd.repositories import dhis2_remote_repository
from dsd.services.dhis2_remote_service import construct_get_element_values_request_query_params

logger = logging.getLogger(__name__)

logger.setLevel(logging.CRITICAL)

FETCH_CUSTOMIZED_RULES_REQUEST_PARAMS = '%sfilter=additionalRuleType:ne:Default' % (
    'fields=%s&'.join(['additionalRuleType', 'additionalRule']))


class DataElementValuesValidationService(object):
    def __init__(self):
        self.alert_should_be_sent = {}.fromkeys(DISEASE_I18N_MAP.keys(), True)
        _, self.rule_group_name_id_map = self.fetch_all_rule_groups()
        self.customized_rules = self.fetch_customized_rules()

    @staticmethod
    def fetch_info_from_updated_data(value):
        year, _, _ = value.bes_year.isocalendar()
        week_time = '%s-W%s' % (year, value.bes_number)

        # date_week_start = datetime.datetime.strptime('%s-0' % week_time, '%Y-W%U-%w').strftime('%Y-%m-%d')
        # date_week_end = datetime.datetime.strptime('%s-6' % week_time, '%Y-W%U-%w').strftime('%Y-%m-%d')

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

    def send_validation_for_each_disease(self, value, organisation_id):
        start, end = self.fetch_info_from_updated_data(value)
        for element_name in DISEASE_I18N_MAP.keys():

            alert_should_be_sent = self.alert_should_be_sent.get(element_name, True)
            rule_group_id = self.get_rule_group_id(element_name)
            response = self.send_validation_request(rule_group_id,
                                                    start,
                                                    end,
                                                    organisation_id,
                                                    alert_should_be_sent)
            if 'validationResults' in response.text:
                logger.critical('validate request success, need to send email.')
                self.alert_should_be_sent[element_name] = False
            elif 'Validation passed successfully' in response.text:
                logger.critical('validate request success, dose not need to send email.')
                self.alert_should_be_sent[element_name] = True

            if response.status_code != HTTP_200_OK:
                logger.critical('validate request failed.')
                pass

    def send_validation_request(self, rule_group_id, start_date, end_date, organisation_id, alert_should_be_sent):
        validate_params = DataElementValuesValidationService.format_validation_request_url(organisation_id, start_date,
                                                                                           end_date, rule_group_id,
                                                                                           alert_should_be_sent)
        return dhis2_remote_repository.get_validation_results(validate_params)

    def send_validation_malaria_in_recent_years_average(self, value, organisation_id):
        current_year, _, _ = value.bes_year.isocalendar()
        week_num = value.bes_number

        rule_type = CUSTOMIZED_VALIDATION_RULE_TYPE.get(MALARIA_CASES)
        weeks_before = self.customized_rules.get(rule_type).get('weeks_before')
        weeks_after = self.customized_rules.get(rule_type).get('weeks_after')
        recent_years = self.customized_rules.get(rule_type).get('recent_years')
        std_dev = self.customized_rules.get(rule_type).get('std_dev')

        malaria_last_five_weeks = self.fetch_malaria_in_previous_weeks(current_year, week_num,
                                                                       weeks_before + weeks_after, organisation_id)
        recent_years_malaria = self.fetch_same_period_in_recent_years(current_year, recent_years, week_num,
                                                                      weeks_before,
                                                                      weeks_after, organisation_id)

        average_malaria_in_recent_years_ = mean(recent_years_malaria)
        std_dev_in_recent_years_malaria = stdev(recent_years_malaria)

        _, data_week_end = self.fetch_info_from_updated_data(value)
        logger.critical('*' * 10)
        logger.critical('data_week_end=%s' % data_week_end)
        start = self.change_date_to_days_before(data_week_end, (weeks_before + weeks_after + 1) * ONE_WEEK_DAYS - 1)

        if malaria_last_five_weeks > average_malaria_in_recent_years_ + std_dev * std_dev_in_recent_years_malaria:
            rule_group_id = self.rule_group_name_id_map.get(
                '%s FIVEYEAR AVAERAGE GROUP' % DISEASE_I18N_MAP.get('malaria'))
            self.send_validation_request(rule_group_id, start, data_week_end, organisation_id, True)

    def send_validation_diarrhea_recent_years_average(self, value, organisation_id):
        current_year, _, _ = value.bes_year.isocalendar()
        week_num = value.bes_number
        recent_years = self.customized_rules.get(CUSTOMIZED_VALIDATION_RULE_TYPE.get(DYSENTERY_CASES)).get(
            'recent_years')
        std_dev = self.customized_rules.get(CUSTOMIZED_VALIDATION_RULE_TYPE.get(DYSENTERY_CASES)).get('std_dev')

        diarrhea_in_current_week = self.fetch_diarrhea_in_week_num(current_year, week_num, organisation_id)
        diarrhea_five_years_same_week = self.fetch_diarrhea_same_week_in_recent_five_years(current_year, recent_years,
                                                                                           week_num, organisation_id)

        average_five_years_diarrhea = mean(diarrhea_five_years_same_week)
        std_dev_five_years_diarrhea = stdev(diarrhea_five_years_same_week)

        data_week_start, data_week_end = self.fetch_info_from_updated_data(value)

        if diarrhea_in_current_week > average_five_years_diarrhea + std_dev * std_dev_five_years_diarrhea:
            rule_group_id = self.rule_group_name_id_map.get(
                '%s FIVEYEAR AVAERAGE GROUP' % DISEASE_I18N_MAP.get('diarrhea'))
            self.send_validation_request(rule_group_id, data_week_start, data_week_end, organisation_id, True)

    def send_validation_for_sarampo_in_recent_weeks(self, value, organisation_id):
        current_year, _, _ = value.bes_year.isocalendar()
        week_num = value.bes_number
        start, end = self.fetch_info_from_updated_data(value)

        week_offset = self.customized_rules.get(CUSTOMIZED_VALIDATION_RULE_TYPE.get(MEASLES_CASES)).get('recent_weeks')
        threshold = self.customized_rules.get(CUSTOMIZED_VALIDATION_RULE_TYPE.get(MEASLES_CASES)).get('threshold')
        sarampo_in_a_month = self.fetch_sarampo_in_a_month(current_year, week_num, week_offset, organisation_id)

        if sarampo_in_a_month >= threshold:
            month_start = self.change_date_to_days_before(start, THREE_WEEKS_DAYS)
            rule_group_id = self.rule_group_name_id_map.get('%s MONTH GROUP' % DISEASE_I18N_MAP.get('measles'))
            self.send_validation_request(rule_group_id, month_start, end, organisation_id, True)

    def send_validation_for_meningitis_every_two_weeks(self, value, organisation_id):
        current_year, _, _ = value.bes_year.isocalendar()
        week_num = value.bes_number

        recent_weeks = self.customized_rules.get(CUSTOMIZED_VALIDATION_RULE_TYPE.get(MENINGITIS_CASES)).get(
            'recent_weeks')
        increased_times = self.customized_rules.get(CUSTOMIZED_VALIDATION_RULE_TYPE.get(MENINGITIS_CASES)).get('times')

        if self.is_meningitis_increasement_rule_match(current_year, week_num, organisation_id, increased_times,
                                                      recent_weeks):
            rule_group_id = self.rule_group_name_id_map.get(
                '%s INCREASEMENT GROUP' % DISEASE_I18N_MAP.get('meningitis'))
            _, data_week_end = self.fetch_info_from_updated_data(value)

            start_before = self.change_date_to_days_before(data_week_end, THREE_WEEKS_DAYS)

            self.send_validation_request(rule_group_id, start_before, data_week_end, organisation_id, True)

    def validate_values(self, date_element_values):
        for value in date_element_values:
            self.send_validation_for_each_disease(value, MOH_UID)

            self.send_validation_for_sarampo_in_recent_weeks(value, MOH_UID)
            self.send_validation_for_meningitis_every_two_weeks(value, MOH_UID)
            self.send_validation_malaria_in_recent_years_average(value, MOH_UID)
            self.send_validation_diarrhea_recent_years_average(value, MOH_UID)

    @staticmethod
    def is_meningitis_increasement_rule_match(year, week, organisation_id, increased_times, week_offset):
        current_year, current_week = DataElementValuesValidationService.calculate_year_week_by_offset(year, week, 0)

        meningitis_cases_current_week = DataElementValuesValidationService.fetch_meningitis(current_year,
                                                                                            current_week,
                                                                                            organisation_id)
        for offset in range(0, -week_offset, -1):
            previous_year, previous_week = DataElementValuesValidationService.calculate_year_week_by_offset(year, week,
                                                                                                            offset - 1)
            meningitis_cases_previous_week = DataElementValuesValidationService.fetch_meningitis(previous_year,
                                                                                                 previous_week,
                                                                                                 organisation_id)
            if meningitis_cases_current_week < meningitis_cases_previous_week * increased_times:
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
        return DataElementValuesValidationService.fetch_disease_in_year_weeks(organisation_id, 'MENINGITE_036',
                                                                              period_weeks)

    @staticmethod
    def fetch_sarampo_in_a_month(year, week_num, week_offset, organisation_id):
        period_weeks = ['%sW%s' % (DataElementValuesValidationService.calculate_year_week_by_offset(year, week_num, i))
                        for i in range(-week_offset + 1, 1)]
        return DataElementValuesValidationService.fetch_disease_in_year_weeks(organisation_id, 'SARAMPO_055',
                                                                              period_weeks)

    @staticmethod
    def fetch_malaria_in_previous_weeks(year, week_num, week_offset, organisation_id):
        period_weeks = ['%sW%s' % (DataElementValuesValidationService.calculate_year_week_by_offset(year, week_num, i))
                        for i in range(-week_offset, 1)]
        return DataElementValuesValidationService.fetch_disease_in_year_weeks(organisation_id, 'MALARIA_084',
                                                                              period_weeks)

    @staticmethod
    def fetch_malaria_by_year_and_weeks_range(year, week_num, weeks_before, after_weeks, organisation_id):
        period_weeks = ['%sW%s' % (DataElementValuesValidationService.calculate_year_week_by_offset(year, week_num, i))
                        for i in range(-weeks_before, after_weeks + 1)]
        return DataElementValuesValidationService.fetch_disease_in_year_weeks(organisation_id, 'MALARIA_084',
                                                                              period_weeks)

    @staticmethod
    def fetch_disease_in_year_weeks(organisation_id, disease_code, period_weeks):
        element_ids = DataElementValuesValidationService.element_id_in_database(disease_code)
        query_params = construct_get_element_values_request_query_params(
            organisation_unit_id=organisation_id,
            element_ids=element_ids,
            period_weeks=period_weeks
        )
        element_datas = dhis2_remote_repository.get_data_element_values(query_params).json().get('rows')
        if not element_ids:
            return 0
        return int(float(element_datas[0][2]))

    @staticmethod
    def element_id_in_database(disease_code):
        return [Element.objects.filter(code=disease_code).first().id]

    @staticmethod
    def fetch_same_period_in_recent_years(current_year, year_offset, week_num, weeks_before, weeks_after,
                                          organisation_id):
        five_years_malaria = []
        for year in range(current_year - year_offset, current_year):
            malaria = DataElementValuesValidationService.fetch_malaria_by_year_and_weeks_range('%s' % year,
                                                                                               week_num, weeks_before,
                                                                                               weeks_after,
                                                                                               organisation_id)
            five_years_malaria.append(malaria)

        return five_years_malaria

    @staticmethod
    def fetch_diarrhea_in_week_num(current_year, week_num, organisation_id):
        period_weeks = ['%sW%s' % (current_year, week_num)]

        return DataElementValuesValidationService.fetch_disease_in_year_weeks(organisation_id, 'DIARREIA_009',
                                                                              period_weeks)

    @staticmethod
    def fetch_diarrhea_same_week_in_recent_five_years(current_year, year_offset, week_num, organisation_id):
        five_years_diarrhea = []

        for year in range(current_year - year_offset, current_year):
            diarrhea = DataElementValuesValidationService.fetch_diarrhea_in_week_num('%s' % year, week_num,
                                                                                     organisation_id)
            five_years_diarrhea.append(diarrhea)
        return five_years_diarrhea

    @staticmethod
    def fetch_customized_rules():
        result = {}
        response_json = dhis2_remote_repository.get_validation_rules(FETCH_CUSTOMIZED_RULES_REQUEST_PARAMS).json()
        for rule in response_json.get('validationRules'):
            result.update({rule.get('additionalRuleType'): rule.get('additionalRule')})
        return result

    @staticmethod
    def extract_params_from_customize_rules():
        customized_rules = DataElementValuesValidationService.fetch_customized_rules()
        result = {}
        for rule_type, rule in customized_rules.items():
            result.update({rule_type: DataElementValuesValidationService.parse_rule_params(rule_type, rule)})
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
        logger.critical(result)
        return result
