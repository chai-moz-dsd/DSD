import uuid

from django.test import TestCase

from dsd.models.remote.sender_from_version_core import SenderFromVersionCore
from dsd.test.factories.sender_from_version_core_factory import SenderFromVersionCoreFactory


class SenderFromVersionCoreTest(TestCase):
    def should_save_sender_from_version_core(self):
        SenderFromVersionCoreFactory(uri=uuid.uuid4())
        self.assertEqual(SenderFromVersionCore.objects.count(), 1)

        SenderFromVersionCoreFactory()
        self.assertEqual(SenderFromVersionCore.objects.count(), 2)

    def should_find_specific_sender_from_version_core(self):
        uri = uuid.uuid4()
        maputo = SenderFromVersionCoreFactory(uri=uri)
        SenderFromVersionCoreFactory()

        actual_sender_from_version_cores = SenderFromVersionCore.objects.filter()
        self.assertEqual(actual_sender_from_version_cores.count(), 2)
        self.assertEqual(actual_sender_from_version_cores[0], maputo)

        actual_sender_from_version_cores = SenderFromVersionCore.objects.filter(uri=uri)
        self.assertEqual(actual_sender_from_version_cores.count(), 1)
        self.assertEqual(actual_sender_from_version_cores[0], maputo)
