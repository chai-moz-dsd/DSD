from django.db import models


class Attribute(models.Model):
    class Meta:
        app_label = 'dsd'

    uid = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    value_type = models.CharField(max_length=255)
    attr_type = models.CharField(max_length=255)
