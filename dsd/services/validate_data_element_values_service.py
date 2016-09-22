import datetime
import logging
import re
from statistics import mean, stdev

import requests
from rest_framework.status import HTTP_200_OK

from chai import settings
from dsd.config.dhis2_config import DISEASE_I18N_MAP, DHIS2_BASE_URL, FOUR_WEEKS_DAYS, SARAMPO_IN_A_MONTH_THRESHOLD, \
    THREE_WEEKS_DAYS, FIVE_WEEKS_DAYS
from dsd.models import Element
from dsd.models.moh import MOH_UID
from dsd.repositories import dhis2_remote_repository
from dsd.repositories.dhis2_remote_repository import get_oauth_header
from dsd.services.dhis2_remote_service import construct_get_element_values_request_query_params

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)


class DataElementValuesValidationService(object):
    def __init__(self):
        self.alert_should_be_sent = {}.fromkeys(DISEASE_I18N_MAP.keys(), True)
        _, self.rule_group_name_id_map = self.fetch_all_rule_groups()

    @staticmethod
    def format_validation_request(organisation_id, start_date, end_date, rule_group_id, alert_should_be_sent):
        alert_flag = 'true' if alert_should_be_sent else 'false'
        validate_request = '%sdhis-web-validationrule/runValidationAction.action?organisationUnitId=%s&startDate=%s&endDate=%s&validationRuleGroupId=%s&sendAlerts=%s' % \
                           (DHIS2_BASE_URL,
                            organisation_id,
                            start_date,
                            end_date,
                            rule_group_id,
                            alert_flag)
        return validate_request

    @staticmethod
    def send_request_to_dhis(dhis2_request):
        return requests.get(dhis2_request,
                            headers=get_oauth_header(),
                            verify=settings.DHIS2_SSL_VERIFY)

    @staticmethod
    def fetch_info_from_updated_data(value):
        organisation_id = MOH_UID
        year, _, _ = value.bes_year.isocalendar()
        week_time = '%s-W%s' % (year, value.bes_number)

        date_week_start = datetime.datetime.strptime('%s-0' % week_time, '%Y-W%U-%w').strftime('%Y-%m-%d')
        date_week_end = datetime.datetime.strptime('%s-6' % week_time, '%Y-W%U-%w').strftime('%Y-%m-%d')

        return date_week_start, date_week_end, organisation_id

    @staticmethod
    def fetch_validation_rule_groups_from_html(html_text):
        validation_rule_groups = {}
        validation_rule_group_pattern = re.compile(r'<tr\sid="tr(\d+)".+data-name="(.+)"')

        for line in html_text.split('\n'):
            ma = re.search(validation_rule_group_pattern, line)
            if ma:
                validation_rule_groups.setdefault(ma.group(2), ma.group(1))

        return validation_rule_groups

    def fetch_all_rule_groups(self):
        rule_groups_url = '%sdhis-web-validationrule/validationRuleGroup.action' % DHIS2_BASE_URL
        response = self.send_request_to_dhis(rule_groups_url)

        return response.status_code, self.fetch_validation_rule_groups_from_html(response.text)

    def get_rule_group_id(self, element_name):
        return self.rule_group_name_id_map.get('%s GROUP' % DISEASE_I18N_MAP.get(element_name))

    def send_validation_for_each_disease(self, start, end, organisation_id):
        for element_name in DISEASE_I18N_MAP.keys():
            alert_should_be_sent = self.alert_should_be_sent.get(element_name, True)
            rule_group_id = self.get_rule_group_id(element_name)
            response = self.send_validation_request(rule_group_id,
                                                    start,
                                                    end,
                                                    organisation_id,
                                                    alert_should_be_sent)

            if 'validationResults' in response.text:
                self.alert_should_be_sent[element_name] = False
            elif 'Validation passed successfully' in response.text:
                self.alert_should_be_sent[element_name] = True

            if response.status_code != HTTP_200_OK:
                logger.critical('validate request failed.')

    def send_validation_request(self, rule_group_id, start, end, organisation_id, alert_should_be_sent):
        validate_request = self.format_validation_request(organisation_id,
                                                          start,
                                                          end,
                                                          rule_group_id,
                                                          alert_should_be_sent)
        response = self.send_request_to_dhis(validate_request)
        return response

    def validate_values(self, date_element_values):
        for value in date_element_values:
            start, end, organisation_id = self.fetch_info_from_updated_data(value)
            self.send_validation_for_each_disease(start, end, organisation_id)

            self.send_validation_for_sarampo_in_a_month(start, end, organisation_id)

            self.send_validation_malaria_fiveyears_average(value, organisation_id)

    @staticmethod
    def change_date_to_days_before(current_date, the_days_before):
        current_date_format = datetime.datetime.strptime(current_date, '%Y-%m-%d')
        before_date = current_date_format - datetime.timedelta(days=the_days_before)
        return before_date.strftime("%Y-%m-%d")

    @staticmethod
    def fetch_sarampo_in_a_month(start, end, organisation_id):
        return 10

    def send_validation_for_sarampo_in_a_month(self, start, end, organisation_id):
        month_start = self.change_date_to_days_before(start, FOUR_WEEKS_DAYS)

        sarampo_in_a_month = self.fetch_sarampo_in_a_month(month_start, end, organisation_id)

        if SARAMPO_IN_A_MONTH_THRESHOLD < sarampo_in_a_month:
            rule_group_id = self.rule_group_name_id_map.get('%s MONTH GROUP' % DISEASE_I18N_MAP.get('measles'))
            self.send_validation_request(rule_group_id, month_start, end, organisation_id, True)

    def send_validation_for_meningitis_every_two_weeks(self, start, end, organisation_id):
        if self.is_meningitis_increasement_rule_match(start, end, organisation_id):
            rule_group_id = self.rule_group_name_id_map.get(
                '%s INCREASEMENT GROUP' % DISEASE_I18N_MAP.get('meningitis'))
            start_before = self.change_date_to_days_before(end, THREE_WEEKS_DAYS)
            self.send_validation_request(rule_group_id, start_before, end, organisation_id, True)

    @staticmethod
    def is_meningitis_increasement_rule_match(year, week, organisation_id):
        meningitis_third_week = DataElementValuesValidationService.fetch_meningitis(year, week, organisation_id)

        target_year, target_week = DataElementValuesValidationService.calculate_year_week_by_offset(year, week, -1)
        meningitis_second_week = DataElementValuesValidationService.fetch_meningitis(target_year, target_week,
                                                                                     organisation_id)
        if meningitis_third_week < meningitis_second_week * 2:
            return False

        target_year, target_week = DataElementValuesValidationService.calculate_year_week_by_offset(year, week, -2)
        meningitis_first_week = DataElementValuesValidationService.fetch_meningitis(target_year, target_week,
                                                                                    organisation_id)

        return meningitis_second_week >= meningitis_first_week * 2

    @staticmethod
    def calculate_year_week_by_offset(current_year, current_week, offset):
        current_week_start_date = datetime.datetime.strptime('%s-W%s-0' % (current_year, current_week), '%Y-W%U-%w')
        target_week_start_date = current_week_start_date + datetime.timedelta(days=offset * 7)
        return int(target_week_start_date.strftime('%Y')), int(target_week_start_date.strftime('%U'))

    @staticmethod
    def fetch_meningitis(year, week, organisation_id):
        element_ids = [Element.objects.filter(code='MENINGITE_036').first().id]
        period_weeks = ['%sW%s' % (year, week)]
        query_params = construct_get_element_values_request_query_params(
            organisation_unit_id=organisation_id,
            element_ids=element_ids,
            period_weeks=period_weeks
        )
        return int(float(dhis2_remote_repository.get_data_element_values(query_params).json().get('rows')[0][2]))

    @staticmethod
    def fetch_malaria_last_five_weeks(year, week):
        return 200

    @staticmethod
    def fetch_malaria_last_year(year, week):
        return 3000

    def send_validation_malaria_fiveyears_average(self, value, organisation_id):
        current_year, _, _ = value.bes_year.isocalendar()
        week_num = value.bes_number

        malaria_last_five_weeks = self.fetch_malaria_last_five_weeks(current_year, week_num)
        five_years_malarias = self.fetch_same_period_in_recent_five_years(current_year, week_num)

        average_five_years_malaria = mean(five_years_malarias)
        std_dev_five_years_malaria = stdev(five_years_malarias)

        _, data_week_end, _ = self.fetch_info_from_updated_data(value)
        start = self.change_date_to_days_before(data_week_end, FIVE_WEEKS_DAYS)

        if malaria_last_five_weeks > average_five_years_malaria + 2 * std_dev_five_years_malaria:
            rule_group_id = self.rule_group_name_id_map.get(
                '%s FIVEYEAR AVAERAGE GROUP' % DISEASE_I18N_MAP.get('malaria'))
            self.send_validation_request(rule_group_id, start, data_week_end, organisation_id, True)

    @staticmethod
    def fetch_same_period_in_recent_five_years(current_year, week_num):

        five_years_malarias = []

        for year in range(current_year - 5, current_year):
            malaria = DataElementValuesValidationService.fetch_malaria_last_year(year=('%s' % year), week=week_num)
            five_years_malarias.append(malaria)

        return five_years_malarias
