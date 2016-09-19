import logging

from django.test import TestCase
from mock import patch, MagicMock
from rest_framework.status import HTTP_200_OK

from dsd.models.moh import MOH_UID
from dsd.services.bes_middleware_core_service import fetch_updated_data_element_values
from dsd.services.validate_data_element_values import DataElementValuesValidation
from dsd.test.factories.bes_middleware_core_factory import BesMiddlewareCoreFactory
from dsd.test.factories.facility_factory import FacilityFactory

logger = logging.getLogger(__name__)

logging.getLogger().setLevel(logging.CRITICAL)


class ValidateDataElementValuesTest(TestCase):
    @patch.object(DataElementValuesValidation, 'fetch_all_rule_groups')
    def setUp(self, mock_fetch_all_rule_groups):
        mock_fetch_all_rule_groups.return_value = (HTTP_200_OK, {})
        self.data_element_values_validation = DataElementValuesValidation()

    def tearDown(self):
        pass

    def test_should_format_validate_request(self):
        expected_validate_request = 'http://52.32.36.132:80/dhis-web-validationrule/runValidationAction.action' \
                                    '?organisationUnitId=MOH12345678&startDate=2016-09-13&endDate=2016-09-13' \
                                    '&validationRuleGroupId=1582&sendAlerts=true'

        validate_request = self.data_element_values_validation.format_validation_request(MOH_UID,
                                                                                         '2016-09-13',
                                                                                         '2016-09-13',
                                                                                         '1582',
                                                                                         True)

        self.assertEqual(validate_request, expected_validate_request)

    @patch('requests.get')
    def test_should_validate_request(self, mock_get):
        mock_get.return_value = MagicMock(status_code=HTTP_200_OK)

        validate_request = self.data_element_values_validation.format_validation_request(MOH_UID,
                                                                                         '2016-09-13',
                                                                                         '2016-09-13',
                                                                                         '1582',
                                                                                         True)
        response = self.data_element_values_validation.send_request_to_dhis(validate_request)
        self.assertEqual(response.status_code, HTTP_200_OK)

    @patch('requests.get')
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

    @patch('requests.get')
    def test_should_validate_data_element_values(self, mock_get):
        device_serial1 = '356670060315512'
        FacilityFactory(device_serial=device_serial1, uid=MOH_UID)
        BesMiddlewareCoreFactory(device_id=device_serial1)
        mock_get.return_value = MagicMock(status_code=HTTP_200_OK, text=REAL_HTML_RESPONSE)

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
                           'MENINGITE GROUP': '1595',
                           'T&Eacute;TANO REC&Eacute;M NASCIDOS GROUP': '1601'}

        rule_groups = self.data_element_values_validation.fetch_validation_rule_groups_from_html(REAL_HTML_RESPONSE)
        self.assertDictEqual(expected_groups, rule_groups)

    @patch('requests.get')
    def test_should_be_false_if_match_rule(self, mock_get):
        mock_get.return_value = MagicMock(status_code=HTTP_200_OK, text='<div id="validationResults">')
        self.data_element_values_validation.send_validation_for_each_disease('2016-09-13',
                                                                             '2016-09-13',
                                                                             MOH_UID)

        self.assertEqual(False, self.data_element_values_validation.alert_should_be_sent['measles'])

    @patch('requests.get')
    def test_should_be_true_if_mismatch_rule(self, mock_get):
        mock_get.return_value = MagicMock(status_code=HTTP_200_OK, text='Validation passed successfully')
        self.data_element_values_validation.send_validation_for_each_disease('2016-09-13',
                                                                             '2016-09-13',
                                                                             MOH_UID)

        self.assertEqual(True, self.data_element_values_validation.alert_should_be_sent['pfa'])


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
