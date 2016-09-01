import logging
from datetime import datetime, timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from dsd.models.remote.province import Province as ProvinceRemote
from dsd.services.province_service import is_updated
from dsd.test.factories.province_factory import ProvinceFactory

logger = logging.getLogger(__name__)


class ProvinceServiceTest(TestCase):
    def test_should_be_false_when_remote_province_updated(self):
        data_creation = datetime.today().date()
        province_remote = ProvinceRemote(province_name='NIASSA', description='description',
                                         data_creation=data_creation, user_creation=1, state=1)
        ProvinceFactory(province_name='NIASSA', description='description',
                        data_creation=data_creation, user_creation=1, state=1)
        self.assertFalse(is_updated(province_remote))

    def test_should_be_true_when_remote_province_description_updated(self):
        data_creation = datetime.today().date()
        province_remote = ProvinceRemote(province_name='NIASSA', description='description123',
                                         data_creation=data_creation, user_creation=1, state=1)
        ProvinceFactory(province_name='NIASSA', description='description',
                        data_creation=data_creation, user_creation=1, state=1)
        self.assertTrue(is_updated(province_remote))

    def test_should_be_true_when_remote_province_data_creation_updated(self):
        data_creation = datetime.today().date()
        province_remote = ProvinceRemote(province_name='NIASSA', description='description',
                                         data_creation=data_creation + timedelta(days=1), user_creation=1, state=1)
        ProvinceFactory(province_name='NIASSA', description='description',
                        data_creation=data_creation, user_creation=1, state=1)
        self.assertTrue(is_updated(province_remote))

    def test_should_be_true_when_remote_province_user_creation_updated(self):
        data_creation = datetime.today().date()
        province_remote = ProvinceRemote(province_name='NIASSA', description='description',
                                         data_creation=data_creation, user_creation=2, state=1)
        ProvinceFactory(province_name='NIASSA', description='description',
                        data_creation=data_creation, user_creation=1, state=1)
        self.assertTrue(is_updated(province_remote))

    def test_should_be_true_when_remote_province_state_updated(self):
        data_creation = datetime.today().date()
        province_remote = ProvinceRemote(province_name='NIASSA', description='description',
                                         data_creation=data_creation, user_creation=1, state=2)
        ProvinceFactory(province_name='NIASSA', description='description',
                        data_creation=data_creation, user_creation=1, state=1)
        self.assertTrue(is_updated(province_remote))

    def test_should_raise_exception_when_remote_province_name_updated(self):
        data_creation = datetime.today().date()
        province_remote = ProvinceRemote(province_name='NIASSA1', description='description',
                                         data_creation=data_creation, user_creation=1, state=1)
        ProvinceFactory(province_name='NIASSA', description='description',
                        data_creation=data_creation, user_creation=1, state=1)

        with self.assertRaises(ObjectDoesNotExist):
            is_updated(province_remote)
