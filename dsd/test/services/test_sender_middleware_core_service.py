import logging
import uuid
from datetime import datetime, timedelta

from django.test import TestCase
from mock import patch

from dsd.models import SenderMiddlewareCore
from dsd.models.remote.sender_middleware_core import SenderMiddlewareCore as SenderMiddlewareCoreRemote
from dsd.services import sender_middleware_core_service
from dsd.services.sender_middleware_core_service import is_valid
from dsd.test.factories.sender_middleware_core_factory import SenderMiddlewareCoreFactory

logger = logging.getLogger(__name__)


class SenderMiddlewareCoreTest(TestCase):
    def test_should_be_false_when_creation_data_after_last_sync_date(self):
        sender_middleware_core = SenderMiddlewareCoreRemote(last_update_date=datetime.now())
        specify_date = datetime.now() + timedelta(days=1)

        self.assertFalse(sender_middleware_core_service.should_be_synced(sender_middleware_core, specify_date))

    def test_should_be_true_when_creation_data_after_last_sync_date(self):
        sender_middleware_core = SenderMiddlewareCoreRemote(last_update_date=datetime.now())
        specify_date = datetime.now() - timedelta(days=1)

        self.assertTrue(sender_middleware_core_service.should_be_synced(sender_middleware_core, specify_date))

    def test_should_be_true_when_sender_middleware_core_is_valid(self):
        self.assertTrue(is_valid(SenderMiddlewareCoreFactory()))

    @patch('dsd.models.remote.sender_middleware_core.SenderMiddlewareCore.objects.all')
    def test_should_sync_all_remote_sender_middleware_core(self, mock_all):
        uuid1 = str(uuid.uuid4())
        mock_all.return_value = [
            SenderMiddlewareCoreRemote(uri=uuid1, creation_date=datetime.now(), last_update_date=datetime.now()),
            SenderMiddlewareCoreRemote(uri=str(uuid.uuid4()), creation_date=datetime.now(),
                                       last_update_date=datetime.now()),
            SenderMiddlewareCoreRemote(uri=str(uuid.uuid4()), creation_date=datetime.now(),
                                       last_update_date=datetime.now()),
            SenderMiddlewareCoreRemote(uri=str(uuid.uuid4()), creation_date=datetime.now(),
                                       last_update_date=datetime.now()),
            SenderMiddlewareCoreRemote(uri=str(uuid.uuid4()), creation_date=datetime.now(),
                                       last_update_date=datetime.now()),
        ]
        sender_middleware_core_service.sync()
        self.assertEqual(SenderMiddlewareCore.objects.count(), 5)
        self.assertEqual(SenderMiddlewareCore.objects.get(uri=uuid1).uri, uuid1)
