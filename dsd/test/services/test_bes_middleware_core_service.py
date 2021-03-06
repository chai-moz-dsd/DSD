import logging
import uuid
from datetime import datetime, timedelta, timezone

from django.test import TestCase
from mock import patch

from dsd.models import BesMiddlewareCore
from dsd.models.remote.bes_middleware_core import BesMiddlewareCore as BesMiddlewareCoreRemote
from dsd.services import bes_middleware_core_service
from dsd.services.bes_middleware_core_service import is_valid
from dsd.test.factories.bes_middleware_core_factory import BesMiddlewareCoreFactory
from dsd.test.factories.facility_factory import FacilityFactory

logger = logging.getLogger(__name__)


class BesMiddlewareCoreTest(TestCase):
    def test_should_be_false_when_creation_data_after_last_sync_date(self):
        bes_middleware_core = BesMiddlewareCoreRemote(middleware_updated_date=datetime.now())
        specify_date = datetime.now() + timedelta(days=1)

        self.assertFalse(bes_middleware_core_service.should_be_synced(bes_middleware_core, specify_date))

    def test_should_be_true_when_creation_data_after_last_sync_date(self):
        bes_middleware_core = BesMiddlewareCoreRemote(middleware_updated_date=datetime.now())
        specify_date = datetime.now() - timedelta(days=1)

        self.assertTrue(bes_middleware_core_service.should_be_synced(bes_middleware_core, specify_date))

    def test_should_be_true_when_bes_middleware_core_is_valid(self):
        self.assertTrue(is_valid(BesMiddlewareCoreFactory()))

    @patch('dsd.models.remote.bes_middleware_core.BesMiddlewareCore.objects.all')
    def test_should_sync_all_remote_bes_middleware_core(self, mock_all):
        uuid1 = str(uuid.uuid4())
        facility_id = 446
        mock_all.return_value.order_by.return_value = [
            BesMiddlewareCoreRemote(middleware_facility_id=facility_id, uri=uuid1,
                                    creation_date=datetime.now(), last_update_date=datetime.now(),
                                    middleware_created_date=datetime.now(), middleware_updated_date=datetime.now()),
            BesMiddlewareCoreRemote(middleware_facility_id=facility_id,
                                    uri=str(uuid.uuid4()), creation_date=datetime.now(),
                                    last_update_date=datetime.now(), middleware_created_date=datetime.now(),
                                    middleware_updated_date=datetime.now()),
            BesMiddlewareCoreRemote(middleware_facility_id=facility_id,
                                    uri=str(uuid.uuid4()), creation_date=datetime.now(),
                                    last_update_date=datetime.now(), middleware_created_date=datetime.now(),
                                    middleware_updated_date=datetime.now()),
            BesMiddlewareCoreRemote(middleware_facility_id=facility_id,
                                    uri=str(uuid.uuid4()), creation_date=datetime.now(),
                                    last_update_date=datetime.now(), middleware_created_date=datetime.now(),
                                    middleware_updated_date=datetime.now()),
            BesMiddlewareCoreRemote(middleware_facility_id=facility_id,
                                    uri=str(uuid.uuid4()), creation_date=datetime.now(),
                                    last_update_date=datetime.now(), middleware_created_date=datetime.now(),
                                    middleware_updated_date=datetime.now()),
        ]

        FacilityFactory(id=facility_id)

        bes_middleware_core_service.sync(None)
        self.assertEqual(BesMiddlewareCore.objects.count(), 5)
        self.assertEqual(BesMiddlewareCore.objects.get(uri=uuid1).uri, uuid1)

    @patch('dsd.models.remote.bes_middleware_core.BesMiddlewareCore.objects.filter')
    def test_should_only_sync_bes_middleware_core_from_last_successful_time(self, mock_filter):
        facility_id1 = 446
        facility_id2 = 447
        mock_filter.return_value.order_by.return_value = [
            BesMiddlewareCoreRemote(middleware_facility_id=facility_id1,
                                    uri=str(uuid.uuid4()),
                                    creation_date=datetime.now(),
                                    last_update_date=datetime.now(), middleware_created_date=datetime.now(),
                                    middleware_updated_date=datetime(2016, 8, 31, 3, 0, 0, 0, timezone.utc)),
            BesMiddlewareCoreRemote(middleware_facility_id=facility_id2,
                                    uri=str(uuid.uuid4()),
                                    creation_date=datetime.now(),
                                    last_update_date=datetime.now(), middleware_created_date=datetime.now(),
                                    middleware_updated_date=datetime(2016, 8, 31, 3, 30, 0, 0, timezone.utc)),
        ]

        FacilityFactory(id=facility_id1)
        FacilityFactory(id=facility_id2)

        bes_middleware_core_service.sync(datetime(2016, 8, 31, 2, 30, 0, 0, timezone.utc))
        self.assertEqual(BesMiddlewareCore.objects.count(), 2)
