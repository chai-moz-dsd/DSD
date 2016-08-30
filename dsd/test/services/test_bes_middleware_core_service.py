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
        bes_middleware_core_service.sync()
        self.assertEqual(BesMiddlewareCore.objects.count(), 5)
        self.assertEqual(BesMiddlewareCore.objects.get(uri=uuid1).uri, uuid1)

    def test_should_build_add_element_value_as_dict(self):
        id_test = generate_id()
        id_test2 = generate_id()
        device_serial = '353288063681856'
        uid = '8dd73ldj0ld'
        name = 'cases_nv_measles'
        name2 = 'cases_anger'
        ElementFactory(name=name, id=id_test)
        ElementFactory(name=name2, id=id_test2)
        FacilityFactory(device_serial=device_serial, uid=uid)
        bes_middleware_core = BesMiddlewareCore(cases_anger=2, cases_nv_measles=5, device_id=device_serial)
        result = bes_middleware_core_service.build_post_data_set_request_body_as_dict(bes_middleware_core)
        self.assertEqual(result.get('orgUnit'), uid)
        self.assertEqual(len(result.get('dataValues')), 2)
        self.assertEqual(result.get('dataValues')[0].get('dataElement'), id_test)
        self.assertEqual(result.get('dataValues')[0].get('value'), 5)
        self.assertEqual(result.get('dataValues')[1].get('dataElement'), id_test2)
        self.assertEqual(result.get('dataValues')[1].get('value'), 2)
