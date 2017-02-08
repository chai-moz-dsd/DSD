import factory

from dsd.models.alert import Alert
from dsd.util.id_generator import generate_id


class AlertFactory(factory.DjangoModelFactory):
    class Meta:
        model = Alert

    rule_group = generate_id()
    rule_type = 4
    org_unit = 25
    should_alert = True
