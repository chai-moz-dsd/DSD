from django.db import models
from django.db.models import CASCADE
from django.utils import timezone
from model_utils.models import TimeStampedModel

from dsd.models import District


class DistrictPopulation(TimeStampedModel):
    class Meta:
        app_label = 'dsd'

    population_size = models.IntegerField(default=0, null=True, unique=True)
    year = models.IntegerField(null=True)
    date_created = models.DateField(default=timezone.now, null=True)
    district = models.OneToOneField(District, on_delete=CASCADE)
