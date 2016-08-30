import logging
from datetime import datetime, timedelta

from django.test import TestCase

from dsd.models.remote.bes_middleware_core import BesMiddlewareCore as BesMiddlewareCoreRemote
from dsd.services import bes_middleware_core_service
from dsd.services.bes_middleware_core_service import is_valid
from dsd.test.factories.bes_middleware_core_factory import BesMiddlewareCoreFactory

logger = logging.getLogger(__name__)


class BesMiddlewareCoreTest(TestCase):
    def test_should_be_false_when_creation_data_after_last_sync_date(self):
        bes_middleware_core = BesMiddlewareCoreRemote(creation_date=datetime.now())
        specify_date = datetime.now() + timedelta(days=1)

        self.assertFalse(bes_middleware_core_service.should_be_synced(bes_middleware_core, specify_date))

    def test_should_be_true_when_creation_data_after_last_sync_date(self):
        bes_middleware_core = BesMiddlewareCoreRemote(creation_date=datetime.now())
        specify_date = datetime.now() - timedelta(days=1)

        self.assertTrue(bes_middleware_core_service.should_be_synced(bes_middleware_core, specify_date))

    def test_should_be_true_when_bes_middleware_core_is_valid(self):
        self.assertTrue(is_valid(BesMiddlewareCoreFactory()))
