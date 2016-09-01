import logging
import uuid
from datetime import datetime, timedelta, timezone

from django.test import TestCase
from mock import patch

from dsd.config import dhis2_config
from dsd.models import BesMiddlewareCore
from dsd.models.remote.bes_middleware_core import BesMiddlewareCore as BesMiddlewareCoreRemote
from dsd.services import bes_middleware_core_service
from dsd.services.bes_middleware_core_service import is_valid, build_data_set_request_body_as_dict
from dsd.test.factories.bes_middleware_core_factory import BesMiddlewareCoreFactory
from dsd.test.factories.element_factory import ElementFactory
from dsd.test.factories.facility_factory import FacilityFactory
from dsd.util.id_generator import generate_id

logger = logging.getLogger(__name__)


class BesMiddlewareCoreTest(TestCase):
    def test_should_be_false_when_creation_data_after_last_sync_date(self):
        bes_middleware_core = BesMiddlewareCoreRemote(last_update_date=datetime.now())
        specify_date = datetime.now() + timedelta(days=1)

        self.assertFalse(bes_middleware_core_service.should_be_synced(bes_middleware_core, specify_date))

    def test_should_be_true_when_creation_data_after_last_sync_date(self):
        bes_middleware_core = BesMiddlewareCoreRemote(last_update_date=datetime.now())
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
        bes_middleware_core_service.sync(None)
        self.assertEqual(BesMiddlewareCore.objects.count(), 5)
        self.assertEqual(BesMiddlewareCore.objects.get(uri=uuid1).uri, uuid1)

    @patch('dsd.models.remote.bes_middleware_core.BesMiddlewareCore.objects.filter')
    @patch('dsd.models.remote.bes_middleware_core.BesMiddlewareCore.objects.all')
    def test_should_only_sync_bes_middleware_core_from_last_successful_time(self, mock_all, mock_filter):
        mock_all.return_value = [
            BesMiddlewareCoreRemote(uri=str(uuid.uuid4()), creation_date=datetime.now(),
                                    last_update_date=datetime(2016, 8, 31, 1, 30, 0, 0, timezone.utc)),
            BesMiddlewareCoreRemote(uri=str(uuid.uuid4()), creation_date=datetime.now(),
                                    last_update_date=datetime(2016, 8, 31, 2, 0, 0, 0, timezone.utc)),
            BesMiddlewareCoreRemote(uri=str(uuid.uuid4()), creation_date=datetime.now(),
                                    last_update_date=datetime(2016, 8, 31, 2, 30, 0, 0, timezone.utc)),
            BesMiddlewareCoreRemote(uri=str(uuid.uuid4()), creation_date=datetime.now(),
                                    last_update_date=datetime(2016, 8, 31, 3, 0, 0, 0, timezone.utc)),
            BesMiddlewareCoreRemote(uri=str(uuid.uuid4()), creation_date=datetime.now(),
                                    last_update_date=datetime(2016, 8, 31, 3, 30, 0, 0, timezone.utc)),
        ]

        mock_filter.return_value = [
            BesMiddlewareCoreRemote(uri=str(uuid.uuid4()), creation_date=datetime.now(),
                                    last_update_date=datetime(2016, 8, 31, 3, 0, 0, 0, timezone.utc)),
            BesMiddlewareCoreRemote(uri=str(uuid.uuid4()), creation_date=datetime.now(),
                                    last_update_date=datetime(2016, 8, 31, 3, 30, 0, 0, timezone.utc)),
        ]

        bes_middleware_core_service.sync(datetime(2016, 8, 31, 2, 30, 0, 0, timezone.utc))
        self.assertEqual(BesMiddlewareCore.objects.count(), 2)

    def test_should_build_add_element_value_as_dict(self):
        id_test = generate_id()
        id_test2 = generate_id()
        device_serial = '353288063681856'
        uid = '8dd73ldj0ld'
        name = 'cases_nv_measles'
        name2 = 'cases_rabies'
        ElementFactory(name=name, id=id_test)
        ElementFactory(name=name2, id=id_test2)
        FacilityFactory(device_serial=device_serial, uid=uid)
        bes_middleware_core = BesMiddlewareCore(cases_rabies=2, cases_nv_measles=5, device_id=device_serial)
        result = bes_middleware_core_service.build_post_data_set_request_body_as_dict(bes_middleware_core)
        self.assertEqual(result.get('orgUnit'), uid)
        self.assertEqual(len(result.get('dataValues')), 2)
        self.assertEqual(result.get('dataValues')[0].get('dataElement'), id_test)
        self.assertEqual(result.get('dataValues')[0].get('value'), 5)
        self.assertEqual(result.get('dataValues')[1].get('dataElement'), id_test2)
        self.assertEqual(result.get('dataValues')[1].get('value'), 2)

    def test_should_build_data_set_request_body_as_dict(self):
        facility1 = FacilityFactory()
        facility2 = FacilityFactory()

        element1 = ElementFactory(id=generate_id())
        element2 = ElementFactory(id=generate_id())

        request_body_dict = build_data_set_request_body_as_dict()

        self.assertEqual(len(request_body_dict.get('dataElements')), 2)
        self.assertEqual(request_body_dict.get('dataElements')[0].get('id'), element1.id)
        self.assertEqual(request_body_dict.get('dataElements')[1].get('id'), element2.id)
        self.assertEqual(request_body_dict.get('name'), dhis2_config.DATA_SET_NAME)
        self.assertEqual(request_body_dict.get('shortName'), dhis2_config.DATA_SET_NAME)

        self.assertEqual(len(request_body_dict.get('organisationUnits')), 2)
        self.assertEqual(request_body_dict.get('organisationUnits')[0].get('id'), facility1.uid)
        self.assertEqual(request_body_dict.get('organisationUnits')[1].get('id'), facility2.uid)
