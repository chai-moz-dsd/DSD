import logging

from django.test import TestCase

from dsd.services.sync.sync_bes_middare_core import is_valid_district
from dsd.test.factories.bes_middleware_core_factory import BesMiddlewareCoreFactory

logger = logging.getLogger(__name__)


class SyncBesMiddleWareCoreTest(TestCase):
    def test_should_be_true_when_bes_middleware_core_is_valid(self):
        self.assertTrue(is_valid_district(BesMiddlewareCoreFactory()))
