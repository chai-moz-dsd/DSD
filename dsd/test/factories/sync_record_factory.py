from datetime import datetime

import factory

from dsd.models import SyncRecord


class SyncRecordFactory(factory.DjangoModelFactory):
    class Meta:
        model = SyncRecord

    created = datetime.now()
    time_start = datetime.now()
    status = 'Success'
