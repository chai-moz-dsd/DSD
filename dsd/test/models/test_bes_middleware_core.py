import uuid

from django.test import TestCase

from dsd.models import BesMiddlewareCore
from dsd.test.factories.bes_middleware_core_factory import BesMiddlewareCoreFactory


class BesMiddlewareCoreTest(TestCase):
    def test_should_save_bes_middleware_core(self):
        BesMiddlewareCoreFactory(uri=uuid.uuid4())
        self.assertEqual(BesMiddlewareCore.objects.count(), 1)

        BesMiddlewareCoreFactory()
        self.assertEqual(BesMiddlewareCore.objects.count(), 2)

    def test_should_find_specific_bes_middleware_core(self):
        uri = str(uuid.uuid4())
        one_record = BesMiddlewareCoreFactory(uri=uri)
        BesMiddlewareCoreFactory()

        actual_base_middleware_cores = BesMiddlewareCore.objects.filter()
        self.assertEqual(actual_base_middleware_cores.count(), 2)
        self.assertEqual(actual_base_middleware_cores[0], one_record)

        actual_base_middleware_cores = BesMiddlewareCore.objects.filter(uri=uri)
        self.assertEqual(actual_base_middleware_cores.count(), 1)
        self.assertEqual(actual_base_middleware_cores[0], one_record)
