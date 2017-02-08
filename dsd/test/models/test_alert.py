from django.test import TestCase

from dsd.models.alert import Alert
from dsd.test.factories.alert_factory import AlertFactory


class AlertTest(TestCase):
    def test_should_save_alert(self):
        AlertFactory()
        self.assertEqual(Alert.objects.count(), 1)

        AlertFactory()
        self.assertEqual(Alert.objects.count(), 2)

    def test_should_get_alert_by_parameters(self):
        rule_group_id = 'Tk0L27C81tj'
        org_unit_uid_1 = 'oc1424e3526'
        org_unit_uid_2 = 'o5737512f8b'

        AlertFactory(rule_group_id=rule_group_id, org_unit_uid=org_unit_uid_1, should_alert=True)
        AlertFactory(rule_group_id=rule_group_id, org_unit_uid=org_unit_uid_2, should_alert=False)

        self.assertEqual(Alert.objects.filter(rule_group_id=rule_group_id, org_unit_uid=org_unit_uid_1).count(), 1)
        self.assertEqual(Alert.objects.filter(rule_group_id=rule_group_id, org_unit_uid=org_unit_uid_2).count(), 1)
        self.assertEqual(Alert.objects.get(rule_group_id=rule_group_id, org_unit_uid=org_unit_uid_1).should_alert, True)
        self.assertEqual(
            Alert.objects.get(rule_group_id=rule_group_id, org_unit_uid=org_unit_uid_2).should_alert, False
        )
