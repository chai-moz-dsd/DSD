from django.db import models
from model_utils.models import TimeStampedModel

from dsd.models import Province


class District(TimeStampedModel):
    class Meta:
        app_label = 'dsd'
        db_table = 'districts'

    uid = models.CharField(max_length=255)
    district_name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, null=True)
    user_creation = models.IntegerField(null=True)
    data_creation = models.DateField(null=True)
    state = models.IntegerField(null=True)
    province = models.ForeignKey(Province)
