from django.core.exceptions import ObjectDoesNotExist

from dsd.models import Alert


def should_send_alert(rule_group_id, org_unit_uid):
    try:
        return Alert.objects.get(rule_group_id=rule_group_id, org_unit_uid=org_unit_uid).should_alert
    except ObjectDoesNotExist:
        update_alert_status(rule_group_id, org_unit_uid, True)
        return True


def update_alert_status(rule_group_id, org_unit_uid, should_alert):
    alerts = Alert.objects.filter(rule_group_id=rule_group_id, org_unit_uid=org_unit_uid)
    amount = alerts.count()

    if 0 == amount:
        Alert(rule_group_id=rule_group_id, org_unit_uid=org_unit_uid, should_alert=should_alert).save()
    elif 1 == amount:
        alert = alerts[0]
        alert.should_alert = should_alert
        alert.save()
    else:
        raise RuntimeError('Should not have more than 1 alert for same organisation unit')
