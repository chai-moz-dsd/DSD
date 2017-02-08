import factory

from dsd.models.alert import Alert
from dsd.util.id_generator import generate_id


class AlertFactory(factory.DjangoModelFactory):
    class Meta:
        model = Alert

    rule_group_id = generate_id()
    org_unit_uid = generate_id()
    should_alert = True
