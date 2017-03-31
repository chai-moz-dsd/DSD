from django.test import TestCase
from rest_framework import status
from mock import patch, MagicMock, Mock

from dsd.services.completeness_service import sql_completeness_case, sql_completeness_sum, \
    sql_facilities_in_area, PROVINCE, DISTRICT, USED_FACILITY_CONDITION
from dsd.test.config import BACKEND_URL

ENDPOINT_URL = BACKEND_URL + 'data_completeness'


class CompletenessDataTest(TestCase):
    def test_should_return_404_with_wrong_api(self):
        response = self.client.get('%s?week=2016W16&ou=MOH' % 'data_fres')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_return_400_with_internal_error(self):
        response = self.client.get('%s?week=2016W16&ous=MOH' % ENDPOINT_URL)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('dsd.api.completeness_selection.fetch_completeness_from_remote_database')
    @patch('dsd.services.completeness_service.fetch_used_facility_from_remote_database')
    @patch('dsd.services.completeness_service.fetch_total_facility_from_remote_database')
    def test_should_response_json_data(self,
                                       mock_fetch_total_facility_from_remote_database,
                                       mock_fetch_used_facility_from_remote_database,
                                       mock_fetch_completeness_from_remote_database):

        mock_response_data = {'total': 180,
                              'mBes': [
                                  {'status': 'completed', 'amount': 30},
                                  {'status': 'incomplete', 'amount': 50},
                                  {'status': 'missing', 'amount': 50}
                              ]}
        mock_fetch_completeness_from_remote_database.return_value = (30, 50, 50)
        mock_fetch_total_facility_from_remote_database.return_value = 180
        mock_fetch_used_facility_from_remote_database.return_value = 130

        response = self.client.get('%s?week=2016W16&ou=MOH12345678' % ENDPOINT_URL)
        self.assertEqual(response.data, mock_response_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_sql_completeness_case(self):
        expected_str = 'CASE WHEN "CASOS_COLERA" != -1 AND "CASOS_COLERA" IS NOT NULL ' \
                       'AND "CASOS_DIARREIA_0_4" != -1 AND "CASOS_DIARREIA_0_4" IS NOT NULL ' \
                       'THEN \'Completed\' ' \
                       'WHEN ( "CASOS_COLERA" = -1 OR "CASOS_COLERA" IS NULL ) ' \
                       'AND ( "CASOS_DIARREIA_0_4" = -1 OR "CASOS_DIARREIA_0_4" IS NULL ) ' \
                       'THEN \'Missing\' ELSE \'Incompleted\' END'

        elements = ['CASOS_COLERA', 'CASOS_DIARREIA_0_4']
        completeness_case = sql_completeness_case(elements)
        self.assertEqual(completeness_case, expected_str)

    def test_sql_completeness_sum(self):
        expected_str = "SUM(CASE WHEN STATUS_TABLE.syncStatus = 'Completed' THEN 1 ELSE 0 END) " \
                       "AS completed, SUM(CASE WHEN STATUS_TABLE.syncStatus = 'Missing' " \
                       "THEN 1 ELSE 0 END) AS missing, SUM(CASE WHEN STATUS_TABLE.syncStatus " \
                       "= 'Incompleted' THEN 1 ELSE 0 END) AS incomplete"

        completeness_sum = sql_completeness_sum('STATUS_TABLE.syncStatus')
        self.assertEqual(completeness_sum, expected_str)

    def test_should_sql_facility_province_be_gaza(self):
        expected_str = 'SELECT COUNT(*) FROM facilities AS f INNER JOIN provinces AS p ON f.province_id = p.id ' \
                       'WHERE p.province_name = \'GAZA\';'
        sql_total_facility = sql_facilities_in_area('GAZA', PROVINCE, '')
        self.assertEqual(sql_total_facility, expected_str)

    def test_should_sql_facility_district_be_gaza(self):
        expected_str = 'SELECT COUNT(*) FROM facilities AS f INNER JOIN districts AS p ON f.district_id = p.id ' \
                       'WHERE p.district_name = \'GAZA\';'
        sql_total_facility = sql_facilities_in_area('GAZA', DISTRICT, '')
        self.assertEqual(sql_total_facility, expected_str)

    def test_should_sql_facility_be_MOH(self):
        expected_str = 'SELECT COUNT(*) FROM facilities;'
        sql_total_facility = sql_facilities_in_area('MOH', None, '')
        self.assertEqual(sql_total_facility, expected_str)

    def test_should_sql_used_facility_province_be_gaza(self):
        expected_str = 'SELECT COUNT(*) FROM facilities AS f INNER JOIN provinces AS p ON f.province_id = p.id ' \
                       'WHERE p.province_name = \'GAZA\' AND device_serial <> \'\';'
        sql_used_facility = sql_facilities_in_area('GAZA', PROVINCE, USED_FACILITY_CONDITION)
        self.assertEqual(sql_used_facility, expected_str)

