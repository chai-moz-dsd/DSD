from django.db import models

from dsd.models import Province


class District(models.Model):
    class Meta:
        app_label = 'dsd'
        db_table = 'districts'

    district_name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, db_column='descricao')
    user_creation = models.IntegerField(db_column='user_criacao')
    data_creation = models.DateField(db_column='data_criacao')
    state = models.IntegerField(db_column='estado')
    province = models.ForeignKey(Province)
