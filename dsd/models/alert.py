from django.db import models
from model_utils.models import TimeStampedModel


class Alert(TimeStampedModel):
    class Meta:
        app_label = 'dsd'

    rule_group = models.CharField(max_length=30, null=False)
    rule_level = models.IntegerField(null=False)
    org_unit = models.IntegerField(null=False)
    should_alert = models.BooleanField(null=False, default=True)
