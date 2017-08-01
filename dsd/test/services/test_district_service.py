import logging
from datetime import datetime, timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from dsd.models import District
from dsd.models.remote.district import District as DistrictRemote
from dsd.services.district_service import is_updated, save_districts
from dsd.test.factories.district_factory import DistrictFactory
from dsd.test.factories.province_factory import ProvinceFactory

logger = logging.getLogger(__name__)


class DistrictServiceTest(TestCase):
    def test_should_be_false_when_remote_district_not_updated(self):
        data_creation = datetime.today().date()
        district_remote = DistrictRemote(id=9999, district_name='NIASSA', description='description',
                                         data_creation=data_creation, user_creation=1, state=1)
        DistrictFactory(id=9999, district_name='NIASSA', description='description',
                        data_creation=data_creation, user_creation=1, state=1)
        self.assertFalse(is_updated(district_remote))

    def test_should_be_true_when_remote_district_description_updated(self):
        data_creation = datetime.today().date()
        district_remote = DistrictRemote(id=9999, district_name='NIASSA', description='description123',
                                         data_creation=data_creation, user_creation=1, state=1)
        DistrictFactory(id=9999, district_name='NIASSA', description='description',
                        data_creation=data_creation, user_creation=1, state=1)
        self.assertTrue(is_updated(district_remote))

    def test_should_be_true_when_remote_district_data_creation_updated(self):
        data_creation = datetime.today().date()
        district_remote = DistrictRemote(id=9999, district_name='NIASSA', description='description',
                                         data_creation=data_creation + timedelta(days=1), user_creation=1, state=1)
        DistrictFactory(id=9999, district_name='NIASSA', description='description',
                        data_creation=data_creation, user_creation=1, state=1)
        self.assertTrue(is_updated(district_remote))

    def test_should_be_true_when_remote_district_user_creation_updated(self):
        data_creation = datetime.today().date()
        district_remote = DistrictRemote(id=9999, district_name='NIASSA', description='description',
                                         data_creation=data_creation, user_creation=2, state=1)
        DistrictFactory(id=9999, district_name='NIASSA', description='description',
                        data_creation=data_creation, user_creation=1, state=1)
        self.assertTrue(is_updated(district_remote))

    def test_should_be_true_when_remote_district_state_updated(self):
        data_creation = datetime.today().date()
        district_remote = DistrictRemote(id=9999, district_name='NIASSA', description='description',
                                         data_creation=data_creation, user_creation=1, state=2)
        DistrictFactory(id=9999, district_name='NIASSA', description='description',
                        data_creation=data_creation, user_creation=1, state=1)
        self.assertTrue(is_updated(district_remote))

    def test_should_create_district(self):
        data_creation = datetime.today().date()
        province = ProvinceFactory()
        district = District(district_name='NIASSA1', description='description',
                            data_creation=data_creation, user_creation=1, state=1,
                            province=province)
        save_districts([district])

        filter_result = District.objects.filter(district_name='NIASSA1')
        self.assertEqual(filter_result.count(), 1)

    def test_should_update_district(self):
        data_creation = datetime.today().date()
        province = ProvinceFactory()
        district = District(id=9999, district_name='NIASSA1', description='description',
                            data_creation=data_creation, user_creation=1, state=1,
                            province=province)
        save_districts([district])

        filter_result = District.objects.filter(district_name='NIASSA1')
        self.assertEqual(filter_result.count(), 1)

        district = District(id=9999, district_name='NIASSA1', description='description2',
                            data_creation=data_creation, user_creation=13, state=12)
        save_districts([district])

        filter_result = District.objects.filter(district_name='NIASSA1')
        self.assertEqual(filter_result.count(), 1)
        self.assertEqual(filter_result[0].description, 'description2')
        self.assertEqual(filter_result[0].user_creation, 13)
        self.assertEqual(filter_result[0].state, 12)

