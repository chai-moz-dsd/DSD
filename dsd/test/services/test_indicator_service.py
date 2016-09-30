from django.test import TestCase

from dsd.api.indicator_endpoint import get_isocalendar
from dsd.services.indicator_service import get_facility_where_clause, get_week_where_clause, get_where_clause


class IndicatorServiceTest(TestCase):

    def test_should_get_isocalendar(self):
        cal_2016_39_3 = get_isocalendar("1475054170024")
        cal_2016_41_5 = get_isocalendar("1476454170024")

        self.assertEqual(cal_2016_39_3, (2016, 39, 3))
        self.assertEqual(cal_2016_41_5, (2016, 41, 5))

    def test_should_get_facilities_where_clause(self):
        facilities = []
        clause = get_facility_where_clause(facilities)
        self.assertEqual(clause, '')

        facilities = ['Facility1']
        clause = get_facility_where_clause(facilities)

        self.assertEqual(clause, '(facility_name = \'Facility1\')')

        facilities = ['Facility1', 'Facility2']
        clause = get_facility_where_clause(facilities)
        self.assertEqual(clause, '(facility_name = \'Facility1\' OR facility_name = \'Facility2\')')

    def test_should_get_week_where_clause(self):
        cal_2016_39_3 = get_isocalendar("1475054170024")
        cal_2016_41_5 = get_isocalendar("1476454170024")

        clause = get_week_where_clause(cal_2016_39_3, cal_2016_41_5)
        self.assertEqual(clause, '("BES_YEAR" = \'2016-01-01\' AND "BES_NUMBER" BETWEEN 39 AND 41)')

        cal_2015_43_3 = get_isocalendar("1445443200000")
        cal_2016_39_5 = get_isocalendar("1475054170024")

        clause = get_week_where_clause(cal_2015_43_3, cal_2016_39_5)
        self.assertEqual(clause, '(("BES_YEAR" = \'2015-01-01\' AND "BES_NUMBER" BETWEEN 43 AND 53) '
                                 'OR ("BES_YEAR" = \'2016-01-01\' AND "BES_NUMBER" BETWEEN 1 AND 39))')

    def test_should_get_where_clause(self):
        facilities = ['Facility1', 'Facility2']
        cal_2015_43_3 = get_isocalendar("1445443200000")
        cal_2016_39_5 = get_isocalendar("1475054170024")

        clause = get_where_clause(facilities, cal_2015_43_3, cal_2016_39_5)
        self.assertEqual(clause, '(facility_name = \'Facility1\' OR facility_name = \'Facility2\')'
                                 ' AND '
                                 '(("BES_YEAR" = \'2015-01-01\' AND "BES_NUMBER" BETWEEN 43 AND 53) '
                                 'OR ("BES_YEAR" = \'2016-01-01\' AND "BES_NUMBER" BETWEEN 1 AND 39))')
