from django.db import models
from model_utils.models import TimeStampedModel


class Alert(TimeStampedModel):
    class Meta:
        app_label = 'dsd'

    rule_group_id = models.CharField(max_length=30, null=False)
    org_unit_uid = models.CharField(max_length=30, null=False)
    should_alert = models.BooleanField(null=False, default=True)
