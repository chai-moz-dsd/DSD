import uuid

from django.test import TestCase

from dsd.models import BesVersionCore
from dsd.test.factories.bes_version_core_factory import BesVersionCoreFactory


class BesVersionCoreTest(TestCase):
    def test_should_save_bes_version_core(self):
        BesVersionCoreFactory(uri=uuid.uuid4())
        self.assertEqual(BesVersionCore.objects.count(), 1)

        BesVersionCoreFactory()
        self.assertEqual(BesVersionCore.objects.count(), 2)

    def test_should_find_specific_bes_version_core(self):
        uri = uuid.uuid4()
        maputo = BesVersionCoreFactory(uri=uri)
        BesVersionCoreFactory()

        actual_base_version_cores = BesVersionCore.objects.filter()
        self.assertEqual(actual_base_version_cores.count(), 2)
        self.assertEqual(actual_base_version_cores[0], maputo)

        actual_base_version_cores = BesVersionCore.objects.filter(uri=uri)
        self.assertEqual(actual_base_version_cores.count(), 1)
        self.assertEqual(actual_base_version_cores[0], maputo)
