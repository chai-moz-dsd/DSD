from django.db import models


class COCRelation(models.Model):
    class Meta:
        app_label = 'dsd'

    name_in_bes = models.CharField(max_length=255, default='')
    element_id = models.CharField(max_length=255, default='')
    cc_id = models.CharField(max_length=255, default='')
    name_of_coc = models.CharField(max_length=255, default='')
    coc_id = models.CharField(max_length=255, default='')
