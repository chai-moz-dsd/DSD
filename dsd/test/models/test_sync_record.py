from datetime import datetime, timezone

from django.test import TestCase

from dsd.models import SyncRecord
from dsd.test.factories.sync_record_factory import SyncRecordFactory


class SyncRecordTest(TestCase):
    def test_should_save_sync_record(self):
        SyncRecordFactory()
        actual_sync_records = SyncRecord.objects.all()

        self.assertEqual(SyncRecord.objects.count(), 1)
        self.assertEqual(actual_sync_records[0].status, 'Success')

    def test_should_get_last_successful_time(self):
        SyncRecordFactory(created=datetime(2016, 8, 31, 2, 30, 0, 0, timezone.utc), status='Success')
        SyncRecordFactory(created=datetime(2016, 8, 31, 3, 0, 0, 0, timezone.utc), status='Failure')

        time = SyncRecord.get_last_successful_sync_time()
        self.assertEqual(time, datetime(2016, 8, 31, 2, 30, 0, 0, timezone.utc))

        SyncRecordFactory(created=datetime(2016, 8, 31, 3, 30, 0, 0, timezone.utc), status='Success')
        SyncRecordFactory(created=datetime(2016, 8, 31, 4, 0, 0, 0, timezone.utc), status='Failure')
        SyncRecordFactory(created=datetime(2016, 8, 31, 4, 30, 0, 0, timezone.utc), status='Failure')

        time = SyncRecord.get_last_successful_sync_time()
        self.assertEqual(time, datetime(2016, 8, 31, 3, 30, 0, 0, timezone.utc))

    def test_should_get_last_successful_time_if_table_is_empty(self):
        time = SyncRecord.get_last_successful_sync_time()

        self.assertIsNone(time)
