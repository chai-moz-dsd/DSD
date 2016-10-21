from django.db import models
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import TimeStampedModel


class SyncRecord(TimeStampedModel):
    STATUS = Choices('Success', 'Failure', 'Not_running')

    time_start = models.DateTimeField(null=True)
    status = StatusField(default=STATUS.Not_running)

    @staticmethod
    def get_fail_instance():
        return SyncRecord(status='Failure')

    @staticmethod
    def get_successful_instance(time_start):
        return SyncRecord(status='Success', time_start=time_start)

    @staticmethod
    def get_last_successful_sync_start_time():
        if not SyncRecord.objects.count():
            return None

        if not SyncRecord.objects.filter(status='Success'):
            return None

        return SyncRecord.objects.filter(status='Success').order_by('-created').first().time_start
