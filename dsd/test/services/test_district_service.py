import logging
from datetime import datetime, timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from dsd.models.remote.district import District as DistrictRemote
from dsd.services.district_service import is_updated
from dsd.test.factories.district_factory import DistrictFactory

logger = logging.getLogger(__name__)


class DistrictServiceTest(TestCase):
    def test_should_be_false_when_remote_district_not_updated(self):
        data_creation = datetime.today().date()
        district_remote = DistrictRemote(district_name='NIASSA', description='description',
                                         data_creation=data_creation, user_creation=1, state=1)
        DistrictFactory(district_name='NIASSA', description='description',
                        data_creation=data_creation, user_creation=1, state=1)
        self.assertFalse(is_updated(district_remote))

    def test_should_be_true_when_remote_district_description_updated(self):
        data_creation = datetime.today().date()
        district_remote = DistrictRemote(district_name='NIASSA', description='description123',
                                         data_creation=data_creation, user_creation=1, state=1)
        DistrictFactory(district_name='NIASSA', description='description',
                        data_creation=data_creation, user_creation=1, state=1)
        self.assertTrue(is_updated(district_remote))

    def test_should_be_true_when_remote_district_data_creation_updated(self):
        data_creation = datetime.today().date()
        district_remote = DistrictRemote(district_name='NIASSA', description='description',
                                         data_creation=data_creation + timedelta(days=1), user_creation=1, state=1)
        DistrictFactory(district_name='NIASSA', description='description',
                        data_creation=data_creation, user_creation=1, state=1)
        self.assertTrue(is_updated(district_remote))

    def test_should_be_true_when_remote_district_user_creation_updated(self):
        data_creation = datetime.today().date()
        district_remote = DistrictRemote(district_name='NIASSA', description='description',
                                         data_creation=data_creation, user_creation=2, state=1)
        DistrictFactory(district_name='NIASSA', description='description',
                        data_creation=data_creation, user_creation=1, state=1)
        self.assertTrue(is_updated(district_remote))

    def test_should_be_true_when_remote_district_state_updated(self):
        data_creation = datetime.today().date()
        district_remote = DistrictRemote(district_name='NIASSA', description='description',
                                         data_creation=data_creation, user_creation=1, state=2)
        DistrictFactory(district_name='NIASSA', description='description',
                        data_creation=data_creation, user_creation=1, state=1)
        self.assertTrue(is_updated(district_remote))

    def test_should_raise_exception_when_remote_district_name_updated(self):
        data_creation = datetime.today().date()
        district_remote = DistrictRemote(district_name='NIASSA1', description='description',
                                         data_creation=data_creation, user_creation=1, state=1)
        DistrictFactory(district_name='NIASSA', description='description',
                        data_creation=data_creation, user_creation=1, state=1)

        with self.assertRaises(ObjectDoesNotExist):
            is_updated(district_remote)
