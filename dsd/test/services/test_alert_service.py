from django.test import TestCase

from dsd.models import Alert
from dsd.services.alert_service import should_send_alert, update_alert_status
from dsd.test.factories.alert_factory import AlertFactory


class AlertServiceTest(TestCase):
    def test_should_get_alert_status(self):
        rule_group_id = 'ahkz0JjYY3U'
        org_unit_uid_1 = 'oc1424e3526'
        org_unit_uid_2 = 'o5737512f8b'
        AlertFactory(rule_group_id=rule_group_id, org_unit_uid=org_unit_uid_1, should_alert=False)
        self.assertEqual(should_send_alert(rule_group_id, org_unit_uid_1), False)
        self.assertEqual(should_send_alert(rule_group_id, org_unit_uid_2), True)
        self.assertEqual(Alert.objects.count(), 2)

    def test_should_update_alert_status(self):
        rule_group_id = 'g0AWTpbBv2o'
        org_unit_uid = 'oc1424e3526'
        AlertFactory(rule_group_id=rule_group_id, org_unit_uid=org_unit_uid, should_alert=False)
        self.assertEqual(should_send_alert(rule_group_id, org_unit_uid), False)

        update_alert_status(rule_group_id, org_unit_uid, True)
        self.assertEqual(should_send_alert(rule_group_id, org_unit_uid), True)
