from django.db import models
from model_utils.models import TimeStampedModel


class Province(TimeStampedModel):
    class Meta:
        app_label = 'dsd'
        db_table = 'provinces'

    uid = models.CharField(max_length=255)
    province_name = models.CharField(max_length=255, unique=True, null=True)
    description = models.CharField(max_length=255, null=True)
    data_creation = models.DateField(null=True)
    user_creation = models.IntegerField(null=True)
    state = models.IntegerField(null=True)
