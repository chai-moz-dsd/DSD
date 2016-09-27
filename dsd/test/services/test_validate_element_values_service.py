import datetime
import logging
import uuid

from django.test import TestCase
from django.test import override_settings
from mock import patch, MagicMock, Mock
from rest_framework.status import HTTP_200_OK

from dsd.config.dhis2_config import FOUR_WEEKS_DAYS
from dsd.models import BesMiddlewareCore
from dsd.models.moh import MOH_UID
from dsd.services.bes_middleware_core_service import fetch_updated_data_element_values
from dsd.services.validate_data_element_values_service import DataElementValuesValidationService
from dsd.test.factories.bes_middleware_core_factory import BesMiddlewareCoreFactory
from dsd.test.factories.element_factory import ElementFactory
from dsd.test.factories.facility_factory import FacilityFactory
from dsd.test.helpers.fake_date import FakeDate

logger = logging.getLogger(__name__)

logging.getLogger().setLevel(logging.CRITICAL)

fetch_disease_in_year_weeks_result = Mock(return_value=10)


class ValidateDataElementValuesServiceTest(TestCase):
    @patch.object(DataElementValuesValidationService, 'send_request_to_dhis')
    def setUp(self, mock_send_request_to_dhis):
        mock_send_request_to_dhis.return_value = MagicMock(status_code=HTTP_200_OK, text=REAL_HTML_RESPONSE)
        self.data_element_values_validation = DataElementValuesValidationService()

    @patch.object(DataElementValuesValidationService, 'fetch_disease_in_year_weeks', fetch_disease_in_year_weeks_result)
    def test_should_fetch_malaria_by_year_two_weeks_wrapped(self):
        self.data_element_values_validation.fetch_malaria_by_year_two_weeks_wrapped(2016, 25, MOH_UID)
        fetch_disease_in_year_weeks_result.assert_called_with(MOH_UID, 'MALARIA_084',
                                                              ['2016W23', '2016W24', '2016W25', '2016W26', '2016W27'])

    def test_should_calculate_year_week_by_offset_minus_1_when_on_year_end(self):
        target_year, target_week = self.data_element_values_validation.calculate_year_week_by_offset(2015, 52, 1)
        self.assertEqual(target_year, 2016)
        self.assertEqual(target_week, 1)

    def test_should_calculate_year_week_by_offset_minus_1_when_on_year_start(self):
        target_year, target_week = self.data_element_values_validation.calculate_year_week_by_offset(2016, 1, -1)
        self.assertEqual(target_year, 2015)
        self.assertEqual(target_week, 52)

    def test_should_calculate_year_week_by_offset_minus_1_when_random_date(self):
        target_year, target_week = self.data_element_values_validation.calculate_year_week_by_offset(2016, 5, -2)
        self.assertEqual(target_year, 2016)
        self.assertEqual(target_week, 3)

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('dsd.repositories.dhis2_remote_repository.get_data_element_values')
    def test_should_fetch_malaria_last_five_weeks(self, mock_get_data_element_values):
        ElementFactory(code='MALARIA_084')
        response = {'rows': [["rf040c9a7ab.GRIMsGFQHUc", "MOH12345678", "15.0"]]}
        mock_get_data_element_values.return_value = MagicMock(json=MagicMock(return_value=response), status_code=200)

        result = DataElementValuesValidationService.fetch_malaria_last_five_weeks(2016, 25, MOH_UID)

        self.assertEqual(result, 15)

    @override_settings(DHIS2_SSL_VERIFY=False)
    @patch('dsd.repositories.dhis2_remote_repository.get_data_element_values')
    def test_should_fetch_meningitis(self, mock_get_data_element_values):
        ElementFactory(code='MENINGITE_036')
        response = {'rows': [["rf040c9a7ab.GRIMsGFQHUc", "MOH12345678", "10.0"]]}
        mock_get_data_element_values.return_value = MagicMock(json=MagicMock(return_value=response), status_code=200)

        result = DataElementValuesValidationService.fetch_meningitis(2016, 25, MOH_UID)

        self.assertEqual(result, 10)

    @patch('datetime.date', FakeDate)
    def test_should_fetch_info_from_updated_data_when_on_random_week(self):
        BesMiddlewareCoreFactory(bes_year=datetime.datetime.today(), bes_number=29)

        value = BesMiddlewareCore.objects.first()
        start, end, _ = self.data_element_values_validation.fetch_info_from_updated_data(value)
        self.assertEqual(start, '2016-07-17')
        self.assertEqual(end, '2016-07-23')

    @patch('datetime.date', FakeDate)
    def test_should_fetch_info_from_updated_data_when_on_year_end(self):
        BesMiddlewareCoreFactory(bes_year=datetime.datetime.today(), bes_number=52)

        value = BesMiddlewareCore.objects.first()
        start, end, _ = self.data_element_values_validation.fetch_info_from_updated_data(value)
        self.assertEqual(start, '2016-12-25')
        self.assertEqual(end, '2016-12-31')

    @patch('datetime.date', FakeDate)
    def test_should_fetch_info_from_updated_data_when_on_year_start(self):
        uri = uuid.uuid4()
        BesMiddlewareCoreFactory(uri=uri, bes_year=datetime.datetime.today(), bes_number=1)
        start, end, _ = self.data_element_values_validation.fetch_info_from_updated_data(
            BesMiddlewareCore.objects.get(uri=uri))
        self.assertEqual(start, '2016-01-03')
        self.assertEqual(end, '2016-01-09')

    def test_should_format_validate_request(self):
        expected_validate_request = 'http://52.32.36.132:80/dhis-web-validationrule/runValidationAction.action' \
                                    '?organisationUnitId=MOH12345678&startDate=2016-09-13&endDate=2016-09-13' \
                                    '&validationRuleGroupId=1582&sendAlerts=true'

        validate_request = DataElementValuesValidationService.format_validation_request_url(MOH_UID,
                                                                                            '2016-09-13',
                                                                                            '2016-09-13',
                                                                                            '1582',
                                                                                            True)

        self.assertEqual(validate_request, expected_validate_request)

    @patch.object(DataElementValuesValidationService, 'send_request_to_dhis')
    def test_should_validate_request(self, mock_get):
        mock_get.return_value = MagicMock(status_code=HTTP_200_OK)

        validate_request = self.data_element_values_validation.format_validation_request_url(MOH_UID,
                                                                                             '2016-09-13',
                                                                                             '2016-09-13',
                                                                                             '1582',
                                                                                             True)
        response = self.data_element_values_validation.send_request_to_dhis(validate_request)
        self.assertEqual(response.status_code, HTTP_200_OK)

    @patch.object(DataElementValuesValidationService, 'send_request_to_dhis')
    def test_should_fetch_all_rule_groups(self, mock_get):
        mock_get.return_value = MagicMock(status_code=HTTP_200_OK)

        status_code, rule_groups = self.data_element_values_validation.fetch_all_rule_groups()
        self.assertEqual(status_code, HTTP_200_OK)

    def test_should_get_rule_group_id_by_rule_name(self):
        expected_group_data_id = '1652'
        rule_name = 'plague'
        with patch.dict(self.data_element_values_validation.rule_group_name_id_map,
                        {'PESTE GROUP': '1652'}):
            self.assertEqual(expected_group_data_id, self.data_element_values_validation.get_rule_group_id(rule_name))

    @patch.object(DataElementValuesValidationService, 'fetch_diarrhea_in_week_num')
    @patch.object(DataElementValuesValidationService, 'fetch_sarampo_in_a_month')
    @patch.object(DataElementValuesValidationService, 'fetch_malaria_by_year_two_weeks_wrapped')
    @patch.object(DataElementValuesValidationService, 'fetch_meningitis')
    @patch.object(DataElementValuesValidationService, 'fetch_malaria_last_five_weeks')
    @patch.object(DataElementValuesValidationService, 'send_request_to_dhis')
    @patch.object(DataElementValuesValidationService, 'send_validation_for_each_disease')
    def test_should_validate_data_element_values(self, mock_send_validation, mock_send_request_to_dhis,
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
        mock_send_request_to_dhis.return_value = MagicMock(status_code=HTTP_200_OK, text=REAL_HTML_RESPONSE)

        data_element_values = fetch_updated_data_element_values()
        self.data_element_values_validation.validate_values(data_element_values)

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

        rule_groups = self.data_element_values_validation.fetch_validation_rule_groups_from_html(REAL_HTML_RESPONSE)
        self.assertDictEqual(expected_groups, rule_groups)

    @patch('datetime.date', FakeDate)
    @patch.object(DataElementValuesValidationService, 'send_request_to_dhis')
    def test_should_be_false_if_match_rule(self, mock_get):
        mock_get.return_value = MagicMock(status_code=HTTP_200_OK, text='<div id="validationResults">')
        BesMiddlewareCoreFactory(bes_year=datetime.datetime.today(), bes_number=52)

        value = BesMiddlewareCore.objects.first()
        self.data_element_values_validation.send_validation_for_each_disease(value, MOH_UID)

        self.assertEqual(False, self.data_element_values_validation.alert_should_be_sent['measles'])

    def test_should_get_four_weeks_before_date(self):
        before_20th = self.data_element_values_validation.change_date_to_days_before('2016-09-20', FOUR_WEEKS_DAYS)
        self.assertEqual(before_20th, '2016-08-24')

        before_08th = self.data_element_values_validation.change_date_to_days_before('2016-08-13', FOUR_WEEKS_DAYS)
        self.assertEqual(before_08th, '2016-07-17')

    @patch('datetime.date', FakeDate)
    @patch.object(DataElementValuesValidationService, 'send_request_to_dhis')
    def test_should_be_true_if_mismatch_rule(self, mock_get):
        mock_get.return_value = MagicMock(status_code=HTTP_200_OK, text='Validation passed successfully')
        BesMiddlewareCoreFactory(bes_year=datetime.datetime.today(), bes_number=52)

        value = BesMiddlewareCore.objects.first()
        self.data_element_values_validation.send_validation_for_each_disease(value, MOH_UID)

        self.assertEqual(True, self.data_element_values_validation.alert_should_be_sent['pfa'])

    @patch.object(DataElementValuesValidationService, 'fetch_sarampo_in_a_month')
    @patch.object(DataElementValuesValidationService, 'send_request_to_dhis')
    def test_should_validate_sarampo_in_a_month(self, mock_send_request_to_dhis, mock_fetch_sarampo_in_a_month):
        mock_send_request_to_dhis.return_value = (HTTP_200_OK, {})
        mock_fetch_sarampo_in_a_month.return_value = 10
        data_element_values = BesMiddlewareCoreFactory(bes_year=datetime.datetime.today(), bes_number=25)
        self.data_element_values_validation.send_validation_for_sarampo_in_a_month(data_element_values, MOH_UID)

        mock_send_request_to_dhis.assert_called_once_with(
            'http://52.32.36.132:80/dhis-web-validationrule/runValidationAction.action' \
            '?organisationUnitId=MOH12345678&startDate=2016-05-23&endDate=2016-06-25' \
            '&validationRuleGroupId=1677&sendAlerts=true')

    @patch.object(DataElementValuesValidationService, 'is_meningitis_increasement_rule_match')
    @patch.object(DataElementValuesValidationService, 'send_request_to_dhis')
    def test_should_validate_meningitis_every_two_weeks(self,
                                                        mock_send_request_to_dhis,
                                                        mock_is_meningitis_increasement_rule_match):
        mock_send_request_to_dhis.return_value = (HTTP_200_OK, {})
        mock_is_meningitis_increasement_rule_match.return_value = True
        data_element_values = BesMiddlewareCoreFactory(bes_year=datetime.datetime.today(), bes_number=25)

        self.data_element_values_validation.send_validation_for_meningitis_every_two_weeks(data_element_values,
                                                                                           MOH_UID)
        mock_send_request_to_dhis.assert_called_once_with(
            'http://52.32.36.132:80/dhis-web-validationrule/runValidationAction.action' \
            '?organisationUnitId=MOH12345678&startDate=2016-06-05&endDate=2016-06-25' \
            '&validationRuleGroupId=1922&sendAlerts=true')

    @patch.object(DataElementValuesValidationService, 'fetch_malaria_by_year_two_weeks_wrapped')
    @patch.object(DataElementValuesValidationService, 'fetch_malaria_last_five_weeks')
    @patch.object(DataElementValuesValidationService, 'send_request_to_dhis')
    def test_should_validate_malaria_five_years_average(self, mock_send_request_to_dhis,
                                                        mocke_fetch_malaria_last_five_weeks,
                                                        mock_fetch_malaria_by_year_two_weeks_wrapped):
        mock_send_request_to_dhis.return_value = (HTTP_200_OK, {})
        mocke_fetch_malaria_last_five_weeks.return_value = 2
        mock_fetch_malaria_by_year_two_weeks_wrapped.return_value = 1
        data_element_values = BesMiddlewareCoreFactory(bes_year=datetime.datetime.today(), bes_number=25)

        self.data_element_values_validation.send_validation_malaria_five_years_average(data_element_values,
                                                                                       MOH_UID)
        mock_send_request_to_dhis.assert_called_once_with(
            'http://52.32.36.132:80/dhis-web-validationrule/runValidationAction.action' \
            '?organisationUnitId=MOH12345678&startDate=2016-05-22&endDate=2016-06-25' \
            '&validationRuleGroupId=1988&sendAlerts=true')

    @patch.object(DataElementValuesValidationService, 'fetch_diarrhea_same_week_in_recent_five_years')
    @patch.object(DataElementValuesValidationService, 'fetch_diarrhea_in_week_num')
    @patch.object(DataElementValuesValidationService, 'send_request_to_dhis')
    def test_should_validate_diarrhea_fiveyears_average(self, mock_send_request_to_dhis,
                                                        mock_fetch_diarrhea_in_week_num,
                                                        mock_fetch_diarrhea_same_week_in_recent_five_years):
        mock_send_request_to_dhis.return_value = (HTTP_200_OK, {})
        mock_fetch_diarrhea_in_week_num.return_value = 2
        mock_fetch_diarrhea_same_week_in_recent_five_years.return_value = [1, 1, 1, 1, 1]
        data_element_values = BesMiddlewareCoreFactory(bes_year=datetime.datetime.today(), bes_number=25)

        self.data_element_values_validation.send_validation_diarrhea_fiveyears_average(data_element_values,
                                                                                       MOH_UID)

        mock_send_request_to_dhis.assert_called_once_with(
            'http://52.32.36.132:80/dhis-web-validationrule/runValidationAction.action' \
            '?organisationUnitId=MOH12345678&startDate=2016-06-19&endDate=2016-06-25' \
            '&validationRuleGroupId=1689&sendAlerts=true')


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
