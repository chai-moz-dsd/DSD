from datetime import datetime

from django.test import TestCase
from mock import patch

from dsd.models import SyncRecord
from dsd.test.factories.sync_record_factory import SyncRecordFactory
from dsd.test.helpers.fake_datetime import FakeDatetime


class SyncRecordTest(TestCase):
    def test_should_save_sync_record(self):
        SyncRecordFactory()
        self.assertEqual(SyncRecord.objects.count(), 1)

    @patch('datetime.datetime', FakeDatetime)
    def test_should_find_specific_sync_record(self):
        SyncRecordFactory()

        actual_sync_records = SyncRecord.objects.filter(last_sync_time=datetime.now())
        self.assertEqual(actual_sync_records.count(), 1)
