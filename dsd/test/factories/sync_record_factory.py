from datetime import datetime

import factory

from dsd.models import SyncRecord


class SyncRecordFactory(factory.DjangoModelFactory):
    class Meta:
        model = SyncRecord

    last_sync_time = datetime.now()
