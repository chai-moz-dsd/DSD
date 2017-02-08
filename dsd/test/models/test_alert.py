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
        AlertFactory(rule_group=rule_group_id, rule_type=4, org_unit=24, should_alert=True)
        AlertFactory(rule_group=rule_group_id, rule_type=4, org_unit=25, should_alert=False)
        AlertFactory(rule_group=rule_group_id, rule_type=3, org_unit=25, should_alert=True)

        self.assertEqual(Alert.objects.filter(rule_group=rule_group_id, rule_type=3).count(), 1)
        self.assertEqual(Alert.objects.filter(rule_group=rule_group_id, rule_type=4).count(), 2)
        self.assertEqual(Alert.objects.get(rule_group=rule_group_id, rule_type=4, org_unit=24).should_alert, True)
        self.assertEqual(Alert.objects.get(rule_group=rule_group_id, rule_type=4, org_unit=25).should_alert, False)
        self.assertEqual(Alert.objects.get(rule_group=rule_group_id, rule_type=3, org_unit=25).should_alert, True)
