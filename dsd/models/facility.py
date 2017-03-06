from django.db import models
from model_utils.models import TimeStampedModel

from dsd.models import District
from dsd.models import Province


class Facility(TimeStampedModel):
    class Meta:
        app_label = 'dsd'

    uid = models.CharField(max_length=255)
    facility_name = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255, null=True)
    longitude = models.CharField(max_length=255, null=True)
    code_us = models.CharField(max_length=255, null=True)
    sorting_us = models.CharField(max_length=255, null=True)
    level_us = models.CharField(max_length=255, null=True)
    fea_us = models.CharField(max_length=255, null=True)
    device_serial = models.CharField(max_length=255, null=True)
    sim_number = models.CharField(max_length=255, null=True)
    sim_serial = models.CharField(max_length=255, null=True)
    device_number = models.CharField(max_length=255, null=True)
    state = models.IntegerField(null=True)

    person_contact_opt = models.CharField(max_length=255, null=True)
    phone_contact_opt = models.CharField(max_length=255, null=True)
    sim_number_opt = models.CharField(max_length=255, null=True)
    sim_serial_opt = models.CharField(max_length=255, null=True)
    mac_number = models.CharField(max_length=255, null=True)
    device_serial_opt = models.CharField(max_length=255, null=True)

    contact_person = models.CharField(max_length=255, null=True)
    phone_contact = models.CharField(max_length=255, null=True)

    province = models.ForeignKey(Province)
    district = models.ForeignKey(District)
