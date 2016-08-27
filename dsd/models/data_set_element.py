import uuid

from django.db import models


class DataSetElement(models.Model):
    class Meta:
        app_label = 'dsd'

    uid = models.CharField(max_length=225, default=str(uuid.uuid4()))
    data_set_id = models.CharField(max_length=255, default=str(uuid.uuid4()))
    complete_data = models.DateField()
    value = models.CharField(max_length=255, default='')
    organization_unit_uid = models.CharField(max_length=255, null=True)
