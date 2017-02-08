from django.test import TestCase

from dsd.models import Alert
from dsd.services.alert_service import should_send_alert, update_alert_status
from dsd.test.factories.alert_factory import AlertFactory


class AlertServiceTest(TestCase):
    def test_should_get_alert_status(self):
        rule_group_id = 'ahkz0JjYY3U'
        AlertFactory(rule_group=rule_group_id, rule_type=4, org_unit=24, should_alert=False)
        self.assertEqual(should_send_alert(rule_group_id, 4, 24), False)
        self.assertEqual(should_send_alert(rule_group_id, 3, 100), True)
        self.assertEqual(Alert.objects.count(), 2)

    def test_should_update_alert_status(self):
        rule_group_id = 'g0AWTpbBv2o'
        AlertFactory(rule_group=rule_group_id, rule_type=4, org_unit=75, should_alert=False)
        self.assertEqual(should_send_alert(rule_group_id, 4, 75), False)

        update_alert_status(rule_group_id, 4, 75, True)
        self.assertEqual(should_send_alert(rule_group_id, 4, 75), True)
