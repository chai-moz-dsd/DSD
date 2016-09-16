import logging
import re

import requests
from rest_framework.status import HTTP_200_OK

from dsd.config.dhis2_config import DISEASE_I18N_MAP, DHIS2_BASE_URL
from dsd.models import Facility
from dsd.models.moh import MOH_UID

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class DataElementValuesValidation(object):
    def __init__(self):
        self.rule_group_name_id_map = {}

        _, rule_groups = self.fetch_all_rule_groups()
        for key, value in rule_groups.items():
            self.rule_group_name_id_map.setdefault(key, value)

    @classmethod
    def format_validate_request(cls, organisation_id, start_date, end_date, rule_group_id):
        validate_request = '%sdhis-web-validationrule/runValidationAction.action?organisationUnitId=%s&startDate=%s&endDate=%s&validationRuleGroupId=%s&sendAlerts=true' % \
                           (DHIS2_BASE_URL,
                            organisation_id,
                            start_date,
                            end_date,
                            rule_group_id)
        return validate_request

    @classmethod
    def do_validation_by_dhis2(cls, validate_request):
        logger.info(validate_request)
        response = requests.get(validate_request, auth=('admin', 'district'))
        if 'validationResults' in response.text:
            logger.info('email need to be send.')
        return response.status_code

    def fetch_all_rule_groups(self):
        rule_groups_url = '%sdhis-web-validationrule/validationRuleGroup.action' % DHIS2_BASE_URL
        response = requests.get(rule_groups_url, auth=('admin', 'district'))

        return response.status_code, self.fetch_validation_rule_groups_from_html(response.text)

    def get_rule_group_id(self, element_name):
        return self.rule_group_name_id_map.get('%s GROUP' % DISEASE_I18N_MAP.get(element_name))

    def validate_values(self, date_element_values):
        for value in date_element_values:
            start, end, organisation_id = self.fetch_info_from_data(value)

            for element_name in DISEASE_I18N_MAP.keys():
                rule_group_id = self.get_rule_group_id(element_name)
                validate_request = self.format_validate_request(organisation_id, start, end, rule_group_id)
                status_code = self.do_validation_by_dhis2(validate_request)

                if status_code != HTTP_200_OK:
                    logger.critical('validate request failed.')

    @classmethod
    def fetch_info_from_data(cls, value):
        # organisation_id = Facility.objects.filter(device_serial=value.device_id).first().uid
        organisation_id = MOH_UID
        date_week_start = value.date_week_start.strftime('%Y-%m-%d')
        date_week_end = value.date_week_end.strftime('%Y-%m-%d')
        logger.info('%s %s' % (date_week_start, date_week_end))

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
