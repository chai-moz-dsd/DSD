import json

import requests
from django.test import TestCase
from mock import MagicMock

from dsd.test.config import BACKEND_URL

ENDPOINT_URL = BACKEND_URL + 'indicator/'


class IndicatorEndpointTest(TestCase):
    def test_should_response_bad_request(self):
        response = self.client.get('%s?startDate=1475054170024&organisationUnits=DESCONHECIDO' % ENDPOINT_URL)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data,
                         'Illegal arguments exception. startDate, endDate, organisationUnits are mandatory.')

        response = self.client.get('%s?startDate=1476454170024&endDate=1475054170024&organisationUnits=DESCONHECIDO'
                                   % ENDPOINT_URL)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'Illegal arguments exception. startDate must less than endDate.')
