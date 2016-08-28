from django.db import models

from dsd.models.remote.province import Province


class District(models.Model):
    class Meta:
        app_label = 'chai'
        db_table = 'districts'

    district_name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, db_column='descricao', null=True)
    user_creation = models.IntegerField(db_column='user_criacao', null=True)
    data_creation = models.DateField(db_column='data_criacao', null=True)
    state = models.IntegerField(db_column='estado', null=True)
    province = models.ForeignKey(Province)
