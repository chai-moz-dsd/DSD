from django.db import models
from django.db.models import CASCADE

from dsd.models import District


class DistrictPopulation(models.Model):
    class Meta:
        app_label = 'chai'
        db_table = 't_district_population'

    population_size = models.IntegerField(null=True)
    year = models.IntegerField(null=True)
    date_created = models.DateField(null=True)
    district = models.OneToOneField(District, on_delete=CASCADE)