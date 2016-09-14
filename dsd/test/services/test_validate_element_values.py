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


class ValidateDataElementValuesTest(TestCase):
    def setUp(self):
        self.data_element_values_validation = DataElementValuesValidation()

    def tearDown(self):
        pass

    def test_should_format_validate_request(self):
        expected_validate_request = 'http://52.32.36.132:80/dhis-web-validationrule/runValidationAction.action' \
                                    '?organisationUnitId=MOH12345678&startDate=2016-09-13&endDate=2016-09-13' \
                                    '&validationRuleGroupId=1582&sendAlerts=true'

        validate_request = self.data_element_values_validation.format_validate_request(MOH_UID, '2016-09-13', '2016-09-13', '1582')

        self.assertEqual(validate_request, expected_validate_request)

    @patch('requests.get')
    def test_should_validate_successful(self, mock_get):
        mock_get.return_value = MagicMock(status_code=HTTP_200_OK)

        validate_request = self.data_element_values_validation.format_validate_request(MOH_UID, '2016-09-13', '2016-09-13', '1582')
        status_code = self.data_element_values_validation.do_validation_by_dhis2(validate_request)
        self.assertEqual(status_code, HTTP_200_OK)

    @patch('requests.get')
    def test_should_fetch_all_rule_groups(self, mock_get):
        mock_get.return_value = MagicMock(status_code=HTTP_200_OK)
        status_code, rule_groups = self.data_element_values_validation.fetch_all_rule_groups()
        self.assertEqual(status_code, HTTP_200_OK)

    def test_should_get_rule_group_id_by_rule_name(self):
        expected_group_data_id = '1676'
        rule_name = 'plague'

        self.assertEqual(expected_group_data_id, self.data_element_values_validation.get_rule_group_id(rule_name))

    def test_should_validate_data_element_values(self):
        device_serial1 = '356670060315512'
        FacilityFactory(device_serial=device_serial1, uid=MOH_UID)
        BesMiddlewareCoreFactory(device_id=device_serial1)

        data_element_values = fetch_updated_data_element_values()
        self.data_element_values_validation.validate_values(data_element_values)

    def test_should_fetch_validation_rule_groups_from_html(self):
        expected_groups = {'PARALISIA FLÁCIDA AGUDA GROUP': '1599',
                           'PESTE GROUP': '1594',
                           'DIARREIA GROUP': '1597',
                           'DISENTERIA GROUP': '1596',
                           'MALÁRIA GROUP': '1600',
                           'RAIVA GROUP': '1598',
                           'CÓLERA GROUP': '1582',
                           'SARAMPO': '1602',
                           'MENINGITE GROUP': '1595',
                           'TÉTANO RECÉM NASCIDOS GROUP': '1601'}
        html_text = '''
        tion clearFilter() {
    jQuery.cookie( "currentPage", null );
    jQuery.cookie( "currentKey", null );
    window.location.href = 'validationRuleGroup.action';
}
</script>
</td>
          <td colspan="3" style="text-align:right"><input type="button" value="Add new" onclick="window.location.href='showAddValidationRuleGroupForm.action'"></td>
        </tr>
			</table>

      <table class="listTable" id="listTable">
        <col>
        <thead>
        <tr>
          <th>Name</th>
        </tr>
        </thead>
        <tbody id="list">
                <tr id="tr1582" data-id="1582" data-uid="xMDPtQycVOY" data-type="ValidationRuleGroup" data-name="CÓLERA GROUP"
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
                <tr id="tr1600" data-id="1600" data-uid="PO2I45E1k4o" data-type="ValidationRuleGroup" data-name="MALÁRIA GROUP"
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
                <tr id="tr1599" data-id="1599" data-uid="aRvXVsoXnwx" data-type="ValidationRuleGroup" data-name="PARALISIA FLÁCIDA AGUDA GROUP"
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
                <tr id="tr1602" data-id="1602" data-uid="TToEcWIrPVp" data-type="ValidationRuleGroup" data-name="SARAMPO"
            data-can-manage="true"
            data-can-update="true"
            data-can-delete="true">
            <td>SARAMPO</td>
        </tr>
                <tr id="tr1601" data-id="1601" data-uid="vQWvq6azBqE" data-type="ValidationRuleGroup" data-name="TÉTANO RECÉM NASCIDOS GROUP"
            data-can-manage="true"
            data-can-update="true"
            data-can-delete="true">
            <td>T&Eacute;TANO REC&Eacute;M NASCIDOS GROUP</td>
        </tr>
                </tbody>
      </table>
			<p></p>
			<div class="paging-container">

	<input type="hidden" id="baseLink" value="/dhis-web-validationrule/validationRuleGroup.action?"/>
	<input type="hidden" id="currentPage" value="1"/>
	<input type="hidden" id="numberOfPages" value="1"/>
			<table style="background-color: #ebf0f6;" width='100%'>
			<
        '''

        rule_groups = self.data_element_values_validation.fetch_validation_rule_groups_from_html(html_text)
        self.assertDictEqual(expected_groups, rule_groups)