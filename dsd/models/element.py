from django.db import models


class Element(models.Model):
    class Meta:
        app_label = 'dsd'

    id = models.CharField(max_length=225, unique=True, primary_key=True)
    aggregation_type = models.CharField(max_length=225, null=True)
    domain_type = models.CharField(max_length=225, null=True)
    value_type = models.CharField(max_length=255, default='')
    code = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255, default='')
    short_name = models.CharField(max_length=255, default='')
