from django.db import models

from dsd.models import CategoryOption


class Category(models.Model):
    class Meta:
        app_label = 'dsd'

    id = models.CharField(max_length=11, unique=True, primary_key=True)
    name = models.CharField(max_length=255, default='')
    category_options = models.ManyToManyField(CategoryOption)
