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

        validate_request = self.data_element_values_validation.format_validate_request(MOH_UID, '2016-09-13',
                                                                                       '2016-09-13', '1582')

        self.assertEqual(validate_request, expected_validate_request)

    @patch('requests.get')
    def test_should_validate_request(self, mock_get):
        mock_get.return_value = MagicMock(status_code=HTTP_200_OK)

        validate_request = self.data_element_values_validation.format_validate_request(MOH_UID, '2016-09-13',
                                                                                       '2016-09-13', '1582')
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


class ValidateDataElementValuesRealRequestTest(TestCase):
    @patch.object(DataElementValuesValidation, 'fetch_info_from_data')
    def test_should_validate_real_data(self, mock_fetch_info_from_data):
        data_element_values_validation = DataElementValuesValidation()

        data_element_values = ['one_mock_value']
        mock_fetch_info_from_data.return_value = ('2015-08-01', '2016-09-01', MOH_UID)

        data_element_values_validation.validate_values(data_element_values)
        logger.info(data_element_values_validation.rule_group_name_id_map)


REAL_HTML_RESPONSE = '''

<!DOCTYPE HTML>
<!--[if IE 7]><html  class="ie7"><![endif]-->
<!--[if IE 8]><html  class="ie8"><![endif]-->
<!--[if IE 9]><html  class="ie9"><![endif]-->
<![if !IE]><html ><![endif]>
  <head>
    <title>DHIS 2</title>
    <meta name="description" content="DHIS 2">
    <meta name="keywords" content="DHIS 2">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <link type="text/css" rel="stylesheet" href="../dhis-web-commons/font-awesome/css/font-awesome.min.css?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"." />
    <link type="text/css" rel="stylesheet" media="screen" href="../dhis-web-commons/javascripts/jQuery/ui/css/redmond/jquery-ui.css?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"." />
    <link type="text/css" rel="stylesheet" media="screen,print" href="../dhis-web-commons/css/light_blue/light_blue.css?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"." />
    <link type="text/css" rel="stylesheet" media="screen,print" href="../dhis-web-commons/css/widgets.css?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"." />
    <link type="text/css" rel="stylesheet" media="print" href="../dhis-web-commons/css/print.css?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"." />
    <link type="text/css" rel="stylesheet" media="screen" href="../dhis-web-commons/javascripts/jQuery/calendars/css/jquery.calendars.picker.css?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"." />
    <link type="text/css" rel="stylesheet" media="screen" href="../dhis-web-commons/select2/select2.css?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"." />
        <link type="text/css" rel="stylesheet" href="../api/files/style?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"." />
    <link rel="shortcut icon" href="../favicon.ico" />
    <!-- Material UI fonts -->
    <link href="../dhis-web-commons/fonts/roboto.css" rel="stylesheet" type="text/css">
    <link href="../dhis-web-commons/material-design-icons/material-icons.css" rel="stylesheet" type="text/css">


    <style>
        html {
            font-size: 14px;
        }

        #header * {
            font-family: 'Roboto';
        }
    </style>

    <script type="text/javascript">
      var dateFormat = 'yy-mm-dd';
    </script>

    <script type="text/javascript" src="../dhis-web-commons/javascripts/es5-shim.min.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/es5-sham.min.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>

    <script type="text/javascript" src="../dhis-web-commons/javascripts/ext/ext-all.js"></script>

    <script type="text/javascript" src="../dhis-web-commons/javascripts/jQuery/jquery.min.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <!-- Menu script is up here due to perceived loading time increase -->
    <script type="text/javascript" src="../dhis-web-commons/javascripts/header-bar/header-bar.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script>
        // Needs to be wrapped in jQuery to be sure the DOM is parsed as the script is not at the bottom.
        jQuery(function () {
            Dhis2HeaderBar.initHeaderBar(document.querySelector('#header'), undefined, { noLoadingIndicator: true });
        });
    </script>
    <!-- // End menu -->
    <!--[if lte IE 8]><script type="text/javascript" src="../dhis-web-commons/javascripts/jQuery/placeholders.jquery.min.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script><![endif]-->
    <script type="text/javascript" src="../dhis-web-commons/javascripts/jQuery/jquery.utils.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/jQuery/jquery.ext.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/jQuery/jquery.metadata.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/jQuery/jquery.tablesorter.min.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/jQuery/jquery.upload-1.0.2.min.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/jQuery/jquery.dhisAjaxSelect.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/jQuery/ui/jquery-ui.min.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/jQuery/ui/jquery.blockUI.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/jQuery/jquery.validate.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/jQuery/jquery.validate.ext.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/jQuery/jquery.cookie.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/jQuery/jquery.glob.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/jQuery/jquery.date.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/jQuery/jquery.tmpl.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/jQuery/jquery.autogrow.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/jQuery/jquery.fileupload.min.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/underscore.min.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/filesize.min.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/dhis2/dhis2.util.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/commons.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/commons.ajax.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/lists.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/periodType.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/date.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/json2.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/validationRules.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/dhis2/dhis2.array.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/dhis2/dhis2.select.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/jQuery/calendars/jquery.calendars.min.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/jQuery/calendars/jquery.calendars.plus.min.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
	<script type="text/javascript" src="../dhis-web-commons/select2/select2.min.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
        <script type="text/javascript" src="../dhis-web-commons/javascripts/dhis2/dhis2.period.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/jQuery/calendars/jquery.calendars.picker.min.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/dhis2/dhis2.selected.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/dhis2/dhis2.comparator.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/dhis2/dhis2.availability.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/dhis2/dhis2.trigger.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/dhis2/dhis2.sharing.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/dhis2/dhis2.validation.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/dhis2/dhis2.storage.ss.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/dhis2/dhis2.storage.ls.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/dhis2/dhis2.storage.idb.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/dhis2/dhis2.storage.memory.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/dhis2/dhis2.storage.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/dhis2/dhis2.contextmenu.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/dhis2/dhis2.appcache.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/javascripts/dhis2/dhis2.translate.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../dhis-web-commons/i18nJavaScript.action?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../main.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <script type="text/javascript" src="../request.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>

    <script type="text/javascript" src="../dhis-web-commons/javascripts/intl-tel-input/js/intlTelInput.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <link type="text/css" rel="stylesheet" href="../dhis-web-commons/javascripts/intl-tel-input/css/intlTelInput.css" />

        <script type="text/javascript" src="javascript/validationRuleGroup.js?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
        <script type="text/javascript" src="../api/files/script?_rev=bzr: ERROR: Not a branch: "/var/jenkins_home/workspace/Dhis2-Src/dhis-2/dhis-services/dhis-service-core/"."></script>
    <!-- Create global system calendar -->
    <script>
      dhis2.period.format = 'yyyy-mm-dd';
            dhis2.period.calendar = $.calendars.instance('gregorian');
            dhis2.period.generator = new dhis2.period.PeriodGenerator( dhis2.period.calendar, dhis2.period.format );
      dhis2.period.picker = new dhis2.period.DatePicker( dhis2.period.calendar, dhis2.period.format );
    </script>
  </head>


  <body>




























    <div id="header">
      <img id="headerBanner" src="../api/staticContent/logo_banner" onclick="window.location.href='../dhis-web-commons-about/redirect.action'" style="cursor:pointer" title="View home page">

      <div id="dhisDropDownMenu"></div>
    </div>
    <span id="showLeftBar">
      <a href="javascript:dhis2.leftBar.showAnimated()" title="Show menu">
        <i class="fa fa-arrow-right leftBarIcon"></i>
      </a>
    </span>

        <div id="leftBar">
      <div id="hideLeftBar">
        <a href="index.action" title="Show main menu" id="showMainMenuLink">
          <i class="fa fa-home leftBarIcon"></i></a>
        <a href="javascript:dhis2.leftBar.hideAnimated()" title="Hide menu" id="hideMainMenuLink">
          <i class="fa fa-arrow-left leftBarIcon"></i></a>
        <a href="javascript:dhis2.leftBar.extendAnimated()" title="Extend menu" id="extendMainMenuLink">
          <i class="fa fa-arrow-right leftBarIcon"></i></a>
      </div>

      <div id="leftBarContents">

<h2>Validation Rule&nbsp;</h2>
<ul>
	<li><a href="validationRule.action">Validation Rule&nbsp;</a></li>	<li><a href="validationRuleGroup.action">Validation Rule Group&nbsp;</a></li></ul>

<h2>Data Analysis&nbsp;</h2>
<ul>
	<li><a href="showRunValidationForm.action">Validation Rule Analysis&nbsp;</a></li>
    <li><a href="viewAnalysisForm.action?key=stddevoutlier">Std Dev Outlier Analysis&nbsp;</a></li>
    <li><a href="viewAnalysisForm.action?key=minmaxoutlier">Min-Max Outlier Analysis&nbsp;</a></li>
    <li><a href="viewFollowupAnalysisForm.action">Follow-Up Analysis&nbsp;</a></li>
</ul>
      </div>
    </div>

    <div id="headerMessage" class="bold"></div>

    <div class="page" id="mainPage"> <!-- Do not set style attr -->


<div id="sharingSettings" title='Sharing settings' style="display: none;" class="page">
    <table style="width: 100%;">
        <tbody>
            <tr>
                <td colspan="2" style="height: 40px"><span class="settingHeader" id="sharingName"></span></td>
            </tr>
            <tr>
                <td><input style="width: 100%;" id="sharingFindUserGroup" placeholder="Search for user groups"/></td>
                <td style="width: 24px;"><button id="addUserGroupAccess" disabled="disabled" style="width:24px; margin-left:2px; text-align:center;">+</button></td>
            </tr>
        </tbody>
    </table>

    <table id="sharingAccessTable" style="width: 100%; margin-top: 6px;">
        <tbody>
        <tr>
        	<td colspan="2" style="padding: 5px 0"><span class="tipText">Created by: </span><span class="tipText" id="sharingUser"></span></td>
        </tr>
        <tr>
        	<td style="width: 300px; padding: 5px 0;">External access (without login)</td>
            <td style="text-align: right;">
                <input id="sharingExternalAccess" type="checkbox" value="true" />
            </td>
            <td style="width: 25px; text-align: center;"></td>
        </tr>
        <tr>
            <td style="width: 300px;">Public access (with login)</td>
            <td>
                <select id="sharingPublicAccess" style="width: 150px;">
                    <option selected="selected" value="--------">None</option>
                    <option value="r-------">Can view</option>
                    <option value="rw------">Can edit and view</option>
                </select>
            </td>
            <td style="width: 25px; text-align: center;"></td>
        </tr>
        </tbody>
    </table>
</div>

<script id="user-group-access-template" type="text/template">
<tr id="<%= id %>">
    <td class="sharingGroupName" style="width: 300px;"><%= label %></td>
    <td>
        <select class="sharingGroupAccess" style="width: 150px;">
            <option value="r-------" <% if(access == 'r-------') { %>selected<% } %>>Can view</option>
            <option value="rw------" <% if(access == 'rw------') { %>selected<% } %>>Can edit and view</option>
        </select>
    </td>
    <td style="width: 25px; text-align: center;"><a href="" class="removeUserGroupAccess">X</a></td>
</tr>
</script>

<script type="text/javascript">
	jQuery(document).ready(function(){
		tableSorter( 'listTable' );

    dhis2.contextmenu.makeContextMenu({
      menuId: 'contextMenu',
      menuItemActiveClass: 'contextMenuItemActive'
    });
	});

  var i18n_confirm_delete = 'Are you sure you want to delete the validation rule group?';
</script>

<h3>Validation rule group management <a href="javascript:getHelpContent('validationRuleGroup')" title="Help"><i class="fa fa-question-circle"></i></a>
</h3>

<div id="contextMenu" class="contextMenu">
  <ul id="contextMenuItems" class="contextMenuItems">
    <li data-enabled="canManage"><a data-target-fn="showSharingDialogWithContext"><i class="fa fa-share"></i>&nbsp;&nbsp;Sharing settings</a></li>
    <li data-enabled="canUpdate"><a data-target-fn="showUpdateValidationRuleGroupForm"><i class="fa fa-edit"></i>&nbsp;&nbsp;Edit</a></li>
    <li data-enabled="canUpdate"><a data-target-fn="translateWithContext"><i class="fa fa-globe"></i>&nbsp;&nbsp;Translate</a></li>
    <li data-enabled="canDelete"><a data-target-fn="removeValidationRuleGroup"><i class="fa fa-trash-o"></i>&nbsp;&nbsp;Remove</a></li>
    <li><a data-target-fn="showValidationRuleGroupDetails"><i class="fa fa-info-circle"></i>&nbsp;&nbsp;Show details</a></li>
  </ul>
</div>

<table class="mainPageTable">
    <tr>
        <td style="vertical-align:top">
			<table width="100%">
				<tr>
          <td><form id="filterKeyForm" action="validationRuleGroup.action" method="GET" onsubmit="submitFilter()">
	<input type="text" id="key" name="key" value="" placeholder="Filter by name" class="filterInput" />
	<input type="hidden" id="curKey" name="curKey" value=""/>
	<input type="submit" id="filterButton" value="Filter" class="filterButton" />
	<input type="button" value="Clear" onclick="javascript:clearFilter()" class="filterButton" />
</form>
<script>
function submitFilter() {
    jQuery.cookie( "currentKey", $( '#key' ).val() );
}

function clearFilter() {
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

	<input type="hidden" id="baseLink" value="/dhis-web-validationrule/validationRuleGroup.action?"/>
	<input type="hidden" id="currentPage" value="1"/>
	<input type="hidden" id="numberOfPages" value="1"/>
			<table style="background-color: #ebf0f6;" width='100%'>
			<tr>
				<td>
					<span>No. of pages:</span> 1
				</td>
				<td>
					<span>No. of rows per page:</span>
					<input type="text" id="sizeOfPage" value="50" style="width:50px" onKeyPress="changePageSize(event);">
				</td>
				<td>
					<span>Jump to page:</span>
					<input type="text" id="jumpToPage" value="1" style="width:50px" onKeyPress="changePageSize(event);">
				</td>
				<td>
					<input type="button" id="submitButton" style='width:40px;' value="Go" onclick="changePageSize(event);">
				</td>
			</tr>
			<tr>
				<td colspan="4"><hr/></td>
			</tr>
			<tr>
			<td colspan="4">
			<div class="paging">
							<span class="first" title="First">&laquo;&laquo;</span>
				<span class="prev" title="Previous">&laquo;</span>

																							<span class="page" title="Page 1">1</span>

							<span class="next" title="Next">&raquo; </span>
				<span class="last" title="Last">&raquo;&raquo;</span>
						</div>

			</td>
			</tr>
		</table>
	</div>

<script>
jQuery.cookie( "currentPage", 1 );</script>
    </td>

    <td id="detailsData">
      <div id="detailsArea">
          <div id="hideDetailsArea">
            <a href="javascript:hideDetails()" title="Hide details"><img src="../images/hide.png" alt="Hide details"></a>
          </div>
          <p><label>Name:</label><br><span id="nameField"></span></p>
          <p><label>Description:</label><br><span id="descriptionField"></span></p>
          <p><label>Number of members:</label><br><span id="memberCountField"></span></p>
          <p><label>Number of user groups to alert:</label><br><span id="userGroupsToAlertCountField"></span></p>
		  <p><label>ID:</label><br><span id="idField"></span></p>
      </div>

			<div id="warningArea">
				<div id="hideDetailsArea">
					<a href="javascript:hideWarning()" title='hide_warning'><img src="../images/hide.png" alt=hide_warning'></a>
				</div>
				<p><span id="warningField"></span></p>
			</div>

    </td>
    </tr>
</table>
          </div>
    <script type="text/javascript">
        </script>

    <div id="rightBar">
      <span id="hideRightBar"><a href="javascript:hideHelpContent()" title="Close">
        <i class="fa fa-times leftBarIcon"></i></a>
      </span>
      <div id="rightBarContents"></div>
    </div>




  </body>
</html>

'''
