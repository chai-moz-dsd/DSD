from django.db import models


class DataSetElement(models.Model):
    class Meta:
        app_label = 'dsd'

    uid = models.CharField(max_length=225)
    data_set_id = models.CharField(max_length=255, unique=True)
    complete_data = models.DateField()
    value = models.CharField(max_length=255, default='')
    organization_unit_uid = models.CharField(max_length=255, null=True)
