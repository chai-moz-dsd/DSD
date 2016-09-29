import datetime
import logging
import uuid

from django.test import TestCase
from django.test import override_settings
from mock import patch, MagicMock, Mock
from rest_framework.status import HTTP_200_OK

from dsd.config.dhis2_config import FOUR_WEEKS_DAYS, MEASLES_CASES, CUSTOMIZED_VALIDATION_RULE_TYPE, \
    MALARIA_CASES, MENINGITIS_CASES, \
    DYSENTERY_CASES
from dsd.models import BesMiddlewareCore
from dsd.models.moh import MOH_UID
from dsd.repositories import dhis2_remote_repository
from dsd.services.bes_middleware_core_service import fetch_updated_data_element_values
from dsd.services.validate_data_element_values_service import DataElementValuesValidationService, \
    FETCH_CUSTOMIZED_RULES_REQUEST_PARAMS
from dsd.test.factories.bes_middleware_core_factory import BesMiddlewareCoreFactory
from dsd.test.factories.element_factory import ElementFactory
from dsd.test.factories.facility_factory import FacilityFactory
from dsd.test.helpers.fake_date import FakeDate

logger = logging.getLogger(__name__)

logging.getLogger().setLevel(logging.CRITICAL)

fetch_disease_in_year_weeks_result = Mock(return_value=10)


class ValidateDataElementValuesServiceTest(TestCase):
    @patch.object(DataElementValuesValidationService, 'fetch_customized_rules')
    @patch('dsd.repositories.dhis2_remote_repository.get_all_rule_groups')
    def setUp(self, mock_get_all_rule_groups, mock_fetch_customized_rules):
        mock_get_all_rule_groups.return_value = MagicMock(status_code=HTTP_200_OK, text=REAL_HTML_RESPONSE)
        mock_fetch_customized_rules.return_value = {
            CUSTOMIZED_VALIDATION_RULE_TYPE.get(MEASLES_CASES): {
                'recent_weeks': 4,
                'threshold': 5
            }
        }
        self.data_element_values_validation_service = DataElementValuesValidationService()

    @patch.object(DataElementValuesValidationService, 'fetch_disease_in_year_weeks', fetch_disease_in_year_weeks_result)
    def test_should_fetch_malaria_by_year_two_weeks_wrapped(self):
        self.data_element_values_validation_service.fetch_malaria_by_year_two_weeks_wrapped(2016, 25, MOH_UID)
        fetch_disease_in_year_weeks_result.assert_called_with(MOH_UID, 'MALARIA_084',
                                                              ['2016W23', '2016W24', '2016W25', '2016W26', '2016W27'])

    def test_should_calculate_year_week_by_offset_minus_1_when_on_year_end(self):
        target_year, target_week = self.data_element_values_validation_service.calculate_year_week_by_offset(2015, 52,
                                                                                                             1)
        self.assertEqual(target_year, 2016)
        self.assertEqual(target_week, 1)

    def test_should_calculate_year_week_by_offset_minus_1_when_on_year_start(self):
        target_year, target_week = self.data_element_values_validation_service.calculate_year_week_by_offset(2016, 1,
                                                                                                             -1)
        self.assertEqual(target_year, 2015)
        self.assertEqual(target_week, 52)

    def test_should_calculate_year_week_by_offset_minus_1_when_random_date(self):
        target_year, target_week = self.data_element_values_validation_service.calculate_year_week_by_offset(2016, 5,
                                                                                                             -2)
        self.assertEqual(target_year, 2016)
        self.assertEqual(target_week, 3)

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('dsd.repositories.dhis2_remote_repository.get_data_element_values')
    def test_should_fetch_malaria_last_five_weeks(self, mock_get_data_element_values):
        ElementFactory(code='MALARIA_084')
        response = {'rows': [["rf040c9a7ab.GRIMsGFQHUc", "MOH12345678", "15.0"]]}
        mock_get_data_element_values.return_value = MagicMock(json=MagicMock(return_value=response),
                                                              status_code=HTTP_200_OK)

        result = DataElementValuesValidationService.fetch_malaria_last_five_weeks(2016, 25, MOH_UID)

        self.assertEqual(result, 15)

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('dsd.repositories.dhis2_remote_repository.get_data_element_values')
    def test_should_fetch_meningitis(self, mock_get_data_element_values):
        ElementFactory(code='MENINGITE_036')
        response = {'rows': [["rf040c9a7ab.GRIMsGFQHUc", "MOH12345678", "10.0"]]}
        mock_get_data_element_values.return_value = MagicMock(json=MagicMock(return_value=response),
                                                              status_code=HTTP_200_OK)

        result = DataElementValuesValidationService.fetch_meningitis(2016, 25, MOH_UID)

        self.assertEqual(result, 10)

    @patch('datetime.date', FakeDate)
    def test_should_fetch_info_from_updated_data_when_on_random_week(self):
        BesMiddlewareCoreFactory(bes_year=datetime.datetime.today(), bes_number=29)

        value = BesMiddlewareCore.objects.first()
        start, end = self.data_element_values_validation_service.fetch_info_from_updated_data(value)
        self.assertEqual(start, '2016-07-18')
        self.assertEqual(end, '2016-07-24')

    @patch('datetime.date', FakeDate)
    def test_should_fetch_info_from_updated_data_when_on_year_end(self):
        BesMiddlewareCoreFactory(bes_year=datetime.datetime.today(), bes_number=52)

        value = BesMiddlewareCore.objects.first()
        start, end = self.data_element_values_validation_service.fetch_info_from_updated_data(value)
        self.assertEqual(start, '2016-12-26')
        self.assertEqual(end, '2017-01-01')

    @patch('datetime.date', FakeDate)
    def test_should_fetch_info_from_updated_data_when_on_year_start(self):
        uri = uuid.uuid4()
        BesMiddlewareCoreFactory(uri=uri, bes_year=datetime.datetime.today(), bes_number=1)
        start, end = self.data_element_values_validation_service.fetch_info_from_updated_data(
            BesMiddlewareCore.objects.get(uri=uri))
        self.assertEqual(start, '2016-01-04')
        self.assertEqual(end, '2016-01-10')

    def test_should_format_validate_request(self):
        expected_validate_request_param = 'organisationUnitId=MOH12345678&startDate=2016-09-13&endDate=2016-09-13' \
                                          '&validationRuleGroupId=1582&sendAlerts=true'

        validate_request = DataElementValuesValidationService.format_validation_request_url(MOH_UID,
                                                                                            '2016-09-13',
                                                                                            '2016-09-13',
                                                                                            '1582',
                                                                                            True)

        self.assertEqual(validate_request, expected_validate_request_param)

    @patch('dsd.repositories.dhis2_remote_repository.get_all_rule_groups')
    def test_should_fetch_all_rule_groups(self, mock_get_all_rule_groups):
        mock_get_all_rule_groups.return_value = MagicMock(status_code=HTTP_200_OK)

        status_code, rule_groups = self.data_element_values_validation_service.fetch_all_rule_groups()
        self.assertEqual(status_code, HTTP_200_OK)

    def test_should_get_rule_group_id_by_rule_name(self):
        expected_group_data_id = '1652'
        rule_name = 'plague'
        with patch.dict(self.data_element_values_validation_service.rule_group_name_id_map,
                        {'PESTE GROUP': '1652'}):
            self.assertEqual(expected_group_data_id,
                             self.data_element_values_validation_service.get_rule_group_id(rule_name))

    @patch.object(DataElementValuesValidationService, 'fetch_diarrhea_in_week_num')
    @patch.object(DataElementValuesValidationService, 'fetch_sarampo_in_a_month')
    @patch.object(DataElementValuesValidationService, 'fetch_malaria_by_year_two_weeks_wrapped')
    @patch.object(DataElementValuesValidationService, 'fetch_meningitis')
    @patch.object(DataElementValuesValidationService, 'fetch_malaria_last_five_weeks')
    @patch('dsd.repositories.dhis2_remote_repository.get_validation_results')
    def test_should_validate_data_element_values(self, mock_get_validation_results,
                                                 mock_fetch_malaria_last_five_weeks, mock_fetch_meningitis,
                                                 mock_fetch_malaria_by_year_two_weeks_wrapped,
                                                 mock_fetch_sarampo_in_a_month,
                                                 mock_fetch_diarrhea_in_week_num):
        mock_fetch_malaria_last_five_weeks.return_value = 50
        mock_fetch_meningitis.return_value = 10
        mock_fetch_malaria_by_year_two_weeks_wrapped.return_value = 10
        mock_fetch_sarampo_in_a_month.return_value = 10
        mock_fetch_diarrhea_in_week_num.return_value = 10

        device_serial1 = '356670060315512'
        FacilityFactory(device_serial=device_serial1, uid=MOH_UID)
        BesMiddlewareCoreFactory(device_id=device_serial1)
        mock_get_validation_results.return_value = MagicMock(status_code=HTTP_200_OK, text=REAL_HTML_RESPONSE)

        data_element_values = fetch_updated_data_element_values()
        self.data_element_values_validation_service.validate_values(data_element_values)

    def test_should_fetch_validation_rule_groups_from_html(self):
        expected_groups = {'PARALISIA FL&Aacute;CIDA AGUDA GROUP': '1599',
                           'PESTE GROUP': '1594',
                           'DIARREIA GROUP': '1597',
                           'DISENTERIA GROUP': '1596',
                           'MAL&Aacute;RIA GROUP': '1600',
                           'RAIVA GROUP': '1598',
                           'C&Oacute;LERA GROUP': '1582',
                           'SARAMPO GROUP': '1602',
                           'SARAMPO MONTH GROUP': '1677',
                           'MENINGITE INCREASEMENT GROUP': '1922',
                           'MAL&Aacute;RIA FIVEYEAR AVAERAGE GROUP': '1988',
                           'DIARREIA FIVEYEAR AVAERAGE GROUP': '1689',
                           'MENINGITE GROUP': '1595',
                           'T&Eacute;TANO REC&Eacute;M NASCIDOS GROUP': '1601'}

        rule_groups = self.data_element_values_validation_service.fetch_validation_rule_groups_from_html(
            REAL_HTML_RESPONSE)
        self.assertDictEqual(expected_groups, rule_groups)

    @patch('datetime.date', FakeDate)
    @patch('dsd.repositories.dhis2_remote_repository.get_validation_results')
    def test_should_be_false_if_match_rule(self, mock_get_validation_results):
        mock_get_validation_results.return_value = MagicMock(status_code=HTTP_200_OK,
                                                             text='<div id="validationResults">')
        BesMiddlewareCoreFactory(bes_year=datetime.datetime.today(), bes_number=52)

        value = BesMiddlewareCore.objects.first()
        self.data_element_values_validation_service.send_validation_for_each_disease(value, MOH_UID)

        self.assertEqual(False, self.data_element_values_validation_service.alert_should_be_sent['measles'])

    def test_should_get_four_weeks_before_date(self):
        before_20th = self.data_element_values_validation_service.change_date_to_days_before('2016-09-20',
                                                                                             FOUR_WEEKS_DAYS)
        self.assertEqual(before_20th, '2016-08-24')

        before_08th = self.data_element_values_validation_service.change_date_to_days_before('2016-08-13',
                                                                                             FOUR_WEEKS_DAYS)
        self.assertEqual(before_08th, '2016-07-17')

    @patch('datetime.date', FakeDate)
    @patch('dsd.repositories.dhis2_remote_repository.get_validation_results')
    def test_should_be_true_if_mismatch_rule(self, mock_get_validation_results):
        mock_get_validation_results.return_value = MagicMock(status_code=HTTP_200_OK,
                                                             text='Validation passed successfully')
        BesMiddlewareCoreFactory(bes_year=datetime.datetime.today(), bes_number=52)

        value = BesMiddlewareCore.objects.first()
        self.data_element_values_validation_service.send_validation_for_each_disease(value, MOH_UID)

        self.assertEqual(True, self.data_element_values_validation_service.alert_should_be_sent['pfa'])

    @patch.object(DataElementValuesValidationService, 'element_id_in_database')
    @patch.object(dhis2_remote_repository, 'get_data_element_values')
    @patch('dsd.repositories.dhis2_remote_repository.get_validation_results')
    def test_should_validate_sarampo_in_a_month(self, mock_get_validation_results,
                                                mock_get_data_element_values,
                                                mock_element_id_in_database):
        mock_get_validation_results.return_value = (HTTP_200_OK, {})
        mock_get_data_element_values.return_value = MagicMock(json=MagicMock(return_value=API_DATA_ELEMENT_RESPONSE),
                                                              status_code=HTTP_200_OK)
        mock_element_id_in_database.return_value = ['1111']
        data_element_values = BesMiddlewareCoreFactory(bes_year=datetime.datetime.today(), bes_number=25)
        self.data_element_values_validation_service.send_validation_for_sarampo_in_a_month(data_element_values, MOH_UID)

        mock_get_validation_results.assert_called_once_with(
            'organisationUnitId=MOH12345678&startDate=2016-05-30&endDate=2016-06-26' \
            '&validationRuleGroupId=1677&sendAlerts=true')

    @patch.object(DataElementValuesValidationService, 'is_meningitis_increasement_rule_match')
    @patch('dsd.repositories.dhis2_remote_repository.get_validation_results')
    def test_should_validate_meningitis_every_two_weeks(self,
                                                        mock_get_validation_results,
                                                        mock_is_meningitis_increasement_rule_match):
        mock_get_validation_results.return_value = (HTTP_200_OK, {})
        mock_is_meningitis_increasement_rule_match.return_value = True
        data_element_values = BesMiddlewareCoreFactory(bes_year=datetime.datetime.today(), bes_number=25)

        self.data_element_values_validation_service.send_validation_for_meningitis_every_two_weeks(data_element_values,
                                                                                                   MOH_UID)
        mock_get_validation_results.assert_called_once_with(
            'organisationUnitId=MOH12345678&startDate=2016-06-05&endDate=2016-06-26' \
            '&validationRuleGroupId=1922&sendAlerts=true')

    @patch.object(DataElementValuesValidationService, 'fetch_malaria_by_year_two_weeks_wrapped')
    @patch.object(DataElementValuesValidationService, 'fetch_malaria_last_five_weeks')
    @patch('dsd.repositories.dhis2_remote_repository.get_validation_results')
    def test_should_validate_malaria_five_years_average(self, mock_get_validation_results,
                                                        mock_fetch_malaria_last_five_weeks,
                                                        mock_fetch_malaria_by_year_two_weeks_wrapped):
        mock_get_validation_results.return_value = (HTTP_200_OK, {})
        mock_fetch_malaria_last_five_weeks.return_value = 2
        mock_fetch_malaria_by_year_two_weeks_wrapped.return_value = 1
        data_element_values = BesMiddlewareCoreFactory(bes_year=datetime.datetime.today(), bes_number=25)

        self.data_element_values_validation_service.send_validation_malaria_five_years_average(data_element_values,
                                                                                               MOH_UID)
        mock_get_validation_results.assert_called_once_with(
            'organisationUnitId=MOH12345678&startDate=2016-05-23&endDate=2016-06-26' \
            '&validationRuleGroupId=1988&sendAlerts=true')

    @patch.object(DataElementValuesValidationService, 'fetch_diarrhea_same_week_in_recent_five_years')
    @patch.object(DataElementValuesValidationService, 'fetch_diarrhea_in_week_num')
    @patch('dsd.repositories.dhis2_remote_repository.get_validation_results')
    def test_should_validate_diarrhea_fiveyears_average(self, mock_get_validation_results,
                                                        mock_fetch_diarrhea_in_week_num,
                                                        mock_fetch_diarrhea_same_week_in_recent_five_years):
        mock_get_validation_results.return_value = (HTTP_200_OK, {})
        mock_fetch_diarrhea_in_week_num.return_value = 2
        mock_fetch_diarrhea_same_week_in_recent_five_years.return_value = [1, 1, 1, 1, 1]
        data_element_values = BesMiddlewareCoreFactory(bes_year=datetime.datetime.today(), bes_number=25)

        self.data_element_values_validation_service.send_validation_diarrhea_fiveyears_average(data_element_values,
                                                                                               MOH_UID)

        mock_get_validation_results.assert_called_once_with(
            'organisationUnitId=MOH12345678&startDate=2016-06-20'
            '&endDate=2016-06-26&validationRuleGroupId=1689&sendAlerts=true')

    @patch('dsd.repositories.dhis2_remote_repository.get_validation_rules')
    def test_should_fetch_all_customized_rules(self, mock_get_validation_rules):
        rules = {
            'validationRules': [
                {
                    'name': 'Sarampo: Cases in recent ( A ) EPI week(s) > ( B )',
                    'additionalRule': 'A: 1\r\nB: 5',
                    'additionalRuleType': CUSTOMIZED_VALIDATION_RULE_TYPE.get(MEASLES_CASES),
                },
                {
                    'name': 'Meningite: Cases increases by ( A ) times in recent ( B ) consecutive weeks',
                    'additionalRule': 'A: 1\r\nB: 5',
                    'additionalRuleType': CUSTOMIZED_VALIDATION_RULE_TYPE.get(MALARIA_CASES),
                },
                {
                    'name': 'Disenteria: Cases > average for same week in last ( A ) years + ( B ) * std dev',
                    'additionalRule': 'A: 1\r\nB: 5',
                    'additionalRuleType': CUSTOMIZED_VALIDATION_RULE_TYPE.get(
                        MENINGITIS_CASES),
                },
                {
                    'name': 'Malária: Cases > average from current week + ( A ) earlier weeks to current week - ( B ) later weeks in past ( C ) years + ( D ) * std dev',
                    'additionalRule': 'A: 1\r\nB: 5',
                    'additionalRuleType': CUSTOMIZED_VALIDATION_RULE_TYPE.get(
                        DYSENTERY_CASES),
                }
            ]
        }
        mock_get_validation_rules.return_value = MagicMock(json=MagicMock(return_value=rules), status_code=HTTP_200_OK)
        result = self.data_element_values_validation_service.fetch_customized_rules()

        self.assertEqual(len(result), 4)
        mock_get_validation_rules.assert_called_once_with(FETCH_CUSTOMIZED_RULES_REQUEST_PARAMS)

    def test_should_parse_params_from_measles_cases_rule(self):
        rule_type = CUSTOMIZED_VALIDATION_RULE_TYPE.get(MEASLES_CASES)
        rule = ' B : 8  \r \n  A : 3 '
        result = self.data_element_values_validation_service.parse_rule_params(rule_type, rule)
        self.assertEqual(len(result), 2)
        self.assertEqual(result.get('recent_weeks'), 3)
        self.assertEqual(result.get('threshold'), 8)

    @patch.object(DataElementValuesValidationService, 'fetch_customized_rules')
    def test_should_extract_params_from_customize_rules(self, mock_fetch_customized_rules):
        rule1 = CUSTOMIZED_VALIDATION_RULE_TYPE.get(MEASLES_CASES)
        rule2 = CUSTOMIZED_VALIDATION_RULE_TYPE.get(MENINGITIS_CASES)
        rule3 = CUSTOMIZED_VALIDATION_RULE_TYPE.get(DYSENTERY_CASES)
        rule4 = CUSTOMIZED_VALIDATION_RULE_TYPE.get(MALARIA_CASES)

        mock_fetch_customized_rules.return_value = {
            rule1: 'A:4\r\nB:5',
            rule2: 'A:2\r\nB:3',
            rule3: 'A:5\r\nB:2',
            rule4: 'A:2\r\nB:2\r\nC:5\r\nD:2',
        }
        result = self.data_element_values_validation_service.extract_params_from_customize_rules()
        logger.critical(result)
        self.assertEqual(len(result.get(rule1)), 2)
        self.assertEqual(result.get(rule1).get('recent_weeks'), 4)
        self.assertEqual(result.get(rule1).get('threshold'), 5)

        self.assertEqual(len(result.get(rule2)), 2)
        self.assertEqual(result.get(rule2).get('recent_weeks'), 3)
        self.assertEqual(result.get(rule2).get('times'), 2)

        self.assertEqual(len(result.get(rule3)), 2)
        self.assertEqual(result.get(rule3).get('recent_years'), 5)
        self.assertEqual(result.get(rule3).get('std_dev'), 2)

        self.assertEqual(len(result.get(rule4)), 4)
        self.assertEqual(result.get(rule4).get('weeks_before'), 2)
        self.assertEqual(result.get(rule4).get('weeks_after'), 2)
        self.assertEqual(result.get(rule4).get('recent_years'), 5)
        self.assertEqual(result.get(rule4).get('std_dev'), 2)


REAL_HTML_RESPONSE = '''

        <tbody id="list">
                <tr id="tr1582" data-id="1582" data-uid="xMDPtQycVOY" data-type="ValidationRuleGroup" data-name="C&Oacute;LERA GROUP"
            data-can-manage="true"
            data-can-update="true"
            data-can-delete="true">
            <td>C&Oacute;LERA GROUP</td>
        </tr>
                <tr id="tr1597" data-id="1597" data-uid="o362a8Q5qdV" data-type="ValidationRuleGroup" data-name="DIARREIA GROUP"
            data-can-manage="true"
            data-can-update="true"
            data-can-delete="true">
            <td>DIARREIA GROUP</td>
        </tr>
                <tr id="tr1596" data-id="1596" data-uid="gXBbM8VQT4k" data-type="ValidationRuleGroup" data-name="DISENTERIA GROUP"
            data-can-manage="true"
            data-can-update="true"
            data-can-delete="true">
            <td>DISENTERIA GROUP</td>
        </tr>
                <tr id="tr1600" data-id="1600" data-uid="PO2I45E1k4o" data-type="ValidationRuleGroup" data-name="MAL&Aacute;RIA GROUP"
            data-can-manage="true"
            data-can-update="true"
            data-can-delete="true">
            <td>MAL&Aacute;RIA GROUP</td>
        </tr>
                <tr id="tr1595" data-id="1595" data-uid="l89OcmVLjYO" data-type="ValidationRuleGroup" data-name="MENINGITE GROUP"
            data-can-manage="true"
            data-can-update="true"
            data-can-delete="true">
            <td>MENINGITE GROUP</td>
        </tr>
                <tr id="tr1599" data-id="1599" data-uid="aRvXVsoXnwx" data-type="ValidationRuleGroup" data-name="PARALISIA FL&Aacute;CIDA AGUDA GROUP"
            data-can-manage="true"
            data-can-update="true"
            data-can-delete="true">
            <td>PARALISIA FL&Aacute;CIDA AGUDA GROUP</td>
        </tr>
                <tr id="tr1594" data-id="1594" data-uid="ln8RIJmI3ff" data-type="ValidationRuleGroup" data-name="PESTE GROUP"
            data-can-manage="true"
            data-can-update="true"
            data-can-delete="true">
            <td>PESTE GROUP</td>
        </tr>
                <tr id="tr1598" data-id="1598" data-uid="an5UpCtRSha" data-type="ValidationRuleGroup" data-name="RAIVA GROUP"
            data-can-manage="true"
            data-can-update="true"
            data-can-delete="true">
            <td>RAIVA GROUP</td>
        </tr>
                <tr id="tr1602" data-id="1602" data-uid="TToEcWIrPVp" data-type="ValidationRuleGroup" data-name="SARAMPO GROUP"
            data-can-manage="true"
            data-can-update="true"
            data-can-delete="true">
            <td>SARAMPO GROUP</td>
        </tr>
                </tr>
                <tr id="tr1677" data-id="1677" data-uid="TToEcWIrPVp" data-type="ValidationRuleGroup" data-name="SARAMPO MONTH GROUP"
            data-can-manage="true"
            data-can-update="true"
            data-can-delete="true">
            <td>SARAMPO MONTH GROUP</td>
        </tr>
                        <tr id="tr1922" data-id="1922" data-uid="TToEcWIrPVp" data-type="ValidationRuleGroup" data-name="MENINGITE INCREASEMENT GROUP"
            data-can-manage="true"
            data-can-update="true"
            data-can-delete="true">
            <td>MENINGITE INCREASEMENT GROUP</td>
        </tr>
                        <tr id="tr1988" data-id="1988" data-uid="TToEcWIrPVp" data-type="ValidationRuleGroup" data-name="MAL&Aacute;RIA FIVEYEAR AVAERAGE GROUP"
            data-can-manage="true"
            data-can-update="true"
            data-can-delete="true">
            <td>MAL&Aacute;RIA FIVEYEAR AVAERAGE GROUP</td>
        </tr>            <tr id="tr1689" data-id="1689" data-uid="TToEcWIrPVp" data-type="ValidationRuleGroup" data-name="DIARREIA FIVEYEAR AVAERAGE GROUP"
            data-can-manage="true"
            data-can-update="true"
            data-can-delete="true">
            <td>DIARREIA FIVEYEAR AVAERAGE GROUP</td>
        </tr>
                <tr id="tr1601" data-id="1601" data-uid="vQWvq6azBqE" data-type="ValidationRuleGroup" data-name="T&Eacute;TANO REC&Eacute;M NASCIDOS GROUP"
            data-can-manage="true"
            data-can-update="true"
            data-can-delete="true">
            <td>T&Eacute;TANO REC&Eacute;M NASCIDOS GROUP</td>
        </tr>
                </tbody>
      </table>
			<p></p>
			<div class="paging-container">


'''

API_DATA_ELEMENT_RESPONSE = {
    "headers": [
        {
            "name": "dx",
            "column": "Data",
            "type": "java.lang.String",
            "hidden": "false",
            "meta": "true"
        },
        {
            "name": "ou",
            "column": "Organisation unit",
            "type": "java.lang.String",
            "hidden": "false",
            "meta": "true"
        },
        {
            "name": "value",
            "column": "Value",
            "type": "java.lang.Double",
            "hidden": "false",
            "meta": "false"
        }
    ],
    "metaData": {
        "names": {
            "rf040c9a7ab": "001 CÓLERA",
            "aPQPkTKqWcM": "C",
            "dx": "Data",
            "2015W25": "2015W25",
            "pe": "Period",
            "ou": "Organisation unit",
            "MOH12345678": "MoH",
            "2015W24": "2015W24",
            "oDqam2UXX9Z": "O"
        },
        "dx": [
            "rf040c9a7ab"
        ],
        "pe": [
            "2015W25",
            "2015W24"
        ],
        "ou": [
            "MOH12345678"
        ],
        "co": [
            "aPQPkTKqWcM",
            "oDqam2UXX9Z"
        ]
    },
    "rows": [
        [
            "rf040c9a7ab",
            "MOH12345678",
            "5.0"
        ]
    ],
    "height": 1,
    "width": 3
}
