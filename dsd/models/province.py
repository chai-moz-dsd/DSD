from django.db import models


class Province(models.Model):
    class Meta:
        app_label = 'dsd'
        db_table = 'provinces'

    province_name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, db_column='descricao')
    data_creation = models.CharField(max_length=255, null=True, db_column='data_criacao')
    user_creation = models.IntegerField(db_column='user_criacao')
    state = models.IntegerField(db_column='estado')
