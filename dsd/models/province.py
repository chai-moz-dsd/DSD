from django.db import models


class Province(models.Model):
    class Meta:
        app_label = 'dsd'
        db_table = 'provinces'

    province_name = models.CharField(max_length=255, unique=True, null=True)
    description = models.CharField(max_length=255, db_column='descricao', null=True)
    data_creation = models.DateField(db_column='data_criacao', null=True)
    user_creation = models.IntegerField(db_column='user_criacao', null=True)
    state = models.IntegerField(db_column='estado', null=True)
