from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import TimeStampedModel


class SyncRecord(TimeStampedModel):
    STATUS = Choices('Success', 'Failure', 'Not_running')

    status = StatusField(default=STATUS.Not_running)

    @staticmethod
    def get_fail_instance():
        return SyncRecord(status='Failure')

    @staticmethod
    def get_successful_instance():
        return SyncRecord(status='Success')

    @staticmethod
    def get_last_successful_sync_time():
        if not SyncRecord.objects.count():
            return None

        if not SyncRecord.objects.filter(status='Success'):
            return None

        return SyncRecord.objects.filter(status='Success').order_by('-created').first().created

