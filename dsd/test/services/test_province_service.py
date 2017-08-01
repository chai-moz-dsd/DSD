import logging
from datetime import datetime, timedelta

from django.test import TestCase

from dsd.models.remote.province import Province as ProvinceRemote
from dsd.services.province_service import is_updated
from dsd.test.factories.province_factory import ProvinceFactory

logger = logging.getLogger(__name__)


class ProvinceServiceTest(TestCase):
    def test_should_be_false_when_remote_province_not_updated(self):
        data_creation = datetime.today().date()
        province_remote = ProvinceRemote(id=9999, province_name='NIASSA', description='description',
                                         data_creation=data_creation, user_creation=1, state=1)
        ProvinceFactory(id=9999, province_name='NIASSA', description='description',
                        data_creation=data_creation, user_creation=1, state=1)
        self.assertFalse(is_updated(province_remote))

    def test_should_be_true_when_remote_province_description_updated(self):
        data_creation = datetime.today().date()
        province_remote = ProvinceRemote(id=9999, province_name='NIASSA', description='description123',
                                         data_creation=data_creation, user_creation=1, state=1)
        ProvinceFactory(id=9999, province_name='NIASSA', description='description',
                        data_creation=data_creation, user_creation=1, state=1)
        self.assertTrue(is_updated(province_remote))

    def test_should_be_true_when_remote_province_data_creation_updated(self):
        data_creation = datetime.today().date()
        province_remote = ProvinceRemote(id=9999, province_name='NIASSA', description='description',
                                         data_creation=data_creation + timedelta(days=1), user_creation=1, state=1)
        ProvinceFactory(id=9999, province_name='NIASSA', description='description',
                        data_creation=data_creation, user_creation=1, state=1)
        self.assertTrue(is_updated(province_remote))

    def test_should_be_true_when_remote_province_user_creation_updated(self):
        data_creation = datetime.today().date()
        province_remote = ProvinceRemote(id=9999, province_name='NIASSA', description='description',
                                         data_creation=data_creation, user_creation=2, state=1)
        ProvinceFactory(id=9999, province_name='NIASSA', description='description',
                        data_creation=data_creation, user_creation=1, state=1)
        self.assertTrue(is_updated(province_remote))

    def test_should_be_true_when_remote_province_state_updated(self):
        data_creation = datetime.today().date()
        province_remote = ProvinceRemote(id=9999, province_name='NIASSA', description='description',
                                         data_creation=data_creation, user_creation=1, state=2)
        ProvinceFactory(id=9999, province_name='NIASSA', description='description',
                        data_creation=data_creation, user_creation=1, state=1)
        self.assertTrue(is_updated(province_remote))
