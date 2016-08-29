from django.db import models

from dsd.models import Province


class District(models.Model):
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
