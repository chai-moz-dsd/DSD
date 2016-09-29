from django.db import models


class HistoricalData(models.Model):
    class Meta:
        app_label = 'chai'
        db_table = 't_historical_data'

    district_id = models.IntegerField(null=True)
    disease_id = models.IntegerField(null=True)
    year = models.IntegerField(null=True)
    week = models.IntegerField(null=True)
    cases = models.IntegerField(null=True)
    deaths = models.IntegerField(null=True)
    date_created = models.DateField(null=True)
    date_updated = models.DateField(null=True)
    status = models.IntegerField(null=True)