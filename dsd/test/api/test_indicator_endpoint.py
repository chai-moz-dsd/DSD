import json

from django.test import TestCase

from dsd.api.indicator_endpoint import get_isoweek
from dsd.test.config import BACKEND_URL

ENDPOINT_URL = BACKEND_URL + 'indicator/'


class IndicatorEndpointTest(TestCase):
    def test_should_response_bad_request(self):
        response = self.client.get('%s?startDate=1475054170024&organisationUnits=DESCONHECIDO' % ENDPOINT_URL)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'Illegal arguments exception. Check the url.')

    def test_should_response_indicator_information_with_one_ou(self):
        response = self.client.get('%s?startDate=1475054170024&endDate=1475054174330&organisationUnits=Facility1'
                                   % ENDPOINT_URL)

        response_dict = json.loads(response.content.decode("utf-8"))
        keys = list(response_dict.keys())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_dict.keys()), 1)
        self.assertEqual(keys[0], 'Facility1')

    def test_should_response_indicator_information_with_multiple_ous(self):
        response = self.client.get(
            '%s?startDate=1475054170024&endDate=1475054174330&organisationUnits=Facility1:Facility2' % ENDPOINT_URL)

        response_dict = json.loads(response.content.decode("utf-8"))
        keys = list(response_dict.keys())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(keys), 2)
        self.assertIn('Facility1', keys)
        self.assertIn('Facility2', keys)

    def test_should_response_indicator_information_with_one_week(self):
        response = self.client.get(
            '%s?startDate=1475054170024&endDate=1475054174330&organisationUnits=Facility1' % ENDPOINT_URL)

        response_dict = json.loads(response.content.decode("utf-8"))
        values = list(response_dict.values())[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(values), 1)

    def test_should_response_indicator_information_with_multiple_weeks(self):
        response = self.client.get(
            '%s?startDate=1475054170024&endDate=1476454170024&organisationUnits=Facility1' % ENDPOINT_URL)

        response_dict = json.loads(response.content.decode("utf-8"))
        values = list(response_dict.values())[0]
        print(values)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(values), 3)

    def test_should_get_isoweek(self):
        week1 = get_isoweek("1475054170024")
        week2 = get_isoweek("1476454170024")

        self.assertEqual(week1, 39)
        self.assertEqual(week2, 41)
