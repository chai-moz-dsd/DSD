import logging
import re

import datetime
import requests
from rest_framework.status import HTTP_200_OK

from chai import settings
from dsd.config.dhis2_config import DISEASE_I18N_MAP, DHIS2_BASE_URL, FOUR_WEEKS_DAYS, SARAMPO_IN_A_MONTH_THRESHOLD
from dsd.models.moh import MOH_UID
from dsd.repositories.dhis2_remote_repository import get_oauth_header

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)


class DataElementValuesValidation(object):
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

    def send_request_to_dhis(cls, rule_groups_url):
        logger.info('-----------------------')
        return requests.get(rule_groups_url,
                            headers=get_oauth_header(),
                            verify=settings.DHIS2_SSL_VERIFY)

    @classmethod
    def fetch_info_from_updated_data(cls, value):
        # organisation_id = Facility.objects.filter(device_serial=value.device_id).first().uid
        organisation_id = MOH_UID
        date_week_start = value.date_week_start.strftime('%Y-%m-%d')
        date_week_end = value.date_week_end.strftime('%Y-%m-%d')

        return date_week_start, date_week_end, organisation_id

    @classmethod
    def fetch_validation_rule_groups_from_html(cls, html_text):
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
            response = self.send_validation_request(element_name, start, end, organisation_id, alert_should_be_sent)

            if 'validationResults' in response.text:
                self.alert_should_be_sent[element_name] = False
            elif 'Validation passed successfully' in response.text:
                self.alert_should_be_sent[element_name] = True

            if response.status_code != HTTP_200_OK:
                logger.critical('validate request failed.')

    def send_validation_request(self, element_name, start, end, organisation_id, alert_should_be_sent):
        rule_group_id = self.get_rule_group_id(element_name)
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

    @classmethod
    def get_four_weeks_before_date(cls, current_date):
        current_date_format = datetime.datetime.strptime(current_date, '%Y-%m-%d')
        before_date = current_date_format - datetime.timedelta(days=FOUR_WEEKS_DAYS)

        return before_date.strftime("%Y-%m-%d")

    @staticmethod
    def fetch_sarampo_in_a_month(start, end, organisation_id):
        return 10

    def send_validation_for_sarampo_in_a_month(self, start, end, organisation_id):
        month_start = self.get_four_weeks_before_date(start)

        sarampo_in_a_month = self.fetch_sarampo_in_a_month(month_start, end, organisation_id)

        if SARAMPO_IN_A_MONTH_THRESHOLD < sarampo_in_a_month:
            self.send_validation_request('measles', month_start, end, organisation_id, True)
