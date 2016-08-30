import uuid

from django.test import TestCase

from dsd.models import SenderMiddlewareCore
from dsd.test.factories.sender_middleware_core_factory import SenderMiddlewareCoreFactory


class SenderMiddlewareCoreTest(TestCase):
    def test_should_save_sender_middleware_core(self):
        SenderMiddlewareCoreFactory(uri=uuid.uuid4())
        self.assertEqual(SenderMiddlewareCore.objects.count(), 1)

        SenderMiddlewareCoreFactory()
        self.assertEqual(SenderMiddlewareCore.objects.count(), 2)

    def test_should_find_specific_sender_middleware_core(self):
        uri = str(uuid.uuid4())
        one_record = SenderMiddlewareCoreFactory(uri=uri)
        SenderMiddlewareCoreFactory()

        actual_sender_middleware_cores = SenderMiddlewareCore.objects.filter()
        self.assertEqual(actual_sender_middleware_cores.count(), 2)

        actual_sender_middleware_cores = SenderMiddlewareCore.objects.filter(uri=uri)
        self.assertEqual(actual_sender_middleware_cores.count(), 1)
        self.assertEqual(actual_sender_middleware_cores[0], one_record)
