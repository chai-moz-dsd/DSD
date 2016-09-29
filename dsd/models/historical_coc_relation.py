from django.db import models

from dsd.models import COCRelation

class HistoricalCOCRelation(models.Model):
    class Meta:
        app_label = 'dsd'

    disease_id = models.IntegerField(default=0, primary_key=True, unique=True)
    disease_name = models.CharField(max_length=255, default='')
    disease_uid = models.CharField(max_length=255, default='')
    cases_coc_id = models.ForeignKey(COCRelation, related_name='cases_coc_id')
    deaths_coc_id = models.ForeignKey(COCRelation, related_name='deaths_coc_id')
