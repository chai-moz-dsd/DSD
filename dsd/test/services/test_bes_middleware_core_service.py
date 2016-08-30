import logging
import uuid
from datetime import datetime, timedelta

from django.test import TestCase
from mock import patch

from dsd.models import BesMiddlewareCore
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

    @patch('dsd.models.remote.bes_middleware_core.BesMiddlewareCore.objects.all')
    def test_should_sync_all_remote_bes_middleware_core(self, mock_all):
        uuid1 = str(uuid.uuid4())
        mock_all.return_value = [
            BesMiddlewareCoreRemote(uri=uuid1, creation_date=datetime.now(), last_update_date=datetime.now()),
            BesMiddlewareCoreRemote(uri=str(uuid.uuid4()), creation_date=datetime.now(),
                                    last_update_date=datetime.now()),
            BesMiddlewareCoreRemote(uri=str(uuid.uuid4()), creation_date=datetime.now(),
                                    last_update_date=datetime.now()),
            BesMiddlewareCoreRemote(uri=str(uuid.uuid4()), creation_date=datetime.now(),
                                    last_update_date=datetime.now()),
            BesMiddlewareCoreRemote(uri=str(uuid.uuid4()), creation_date=datetime.now(),
                                    last_update_date=datetime.now()),
        ]
        bes_middleware_core_service.sync()
        self.assertEqual(BesMiddlewareCore.objects.count(), 5)
        self.assertEqual(BesMiddlewareCore.objects.all().first().uri, uuid1)
