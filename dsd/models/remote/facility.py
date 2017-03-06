from django.db import models

from dsd.models.remote.district import District
from dsd.models.remote.province import Province


class Facility(models.Model):
    class Meta:
        app_label = 'chai'
        db_table = 'facilities'

    facility_name = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255, null=True)
    longitude = models.CharField(max_length=255, null=True)
    code_us = models.CharField(max_length=255, null=True)
    sorting_us = models.CharField(max_length=255, db_column='classificacao_us', null=True)
    level_us = models.CharField(max_length=255, db_column='nivel_us', null=True)
    fea_us = models.CharField(max_length=255, db_column='fea_us', null=True)
    device_serial = models.CharField(max_length=255, null=True)
    sim_number = models.CharField(max_length=255, db_column='sim_numb', null=True)
    sim_serial = models.CharField(max_length=255, null=True)
    device_number = models.CharField(max_length=255, db_column='device_numb', null=True)
    state = models.IntegerField(db_column='estado', null=True)

    person_contact_opt = models.CharField(max_length=255, db_column='pessoa_contacto_opt', null=True)
    phone_contact_opt = models.CharField(max_length=255, db_column='telefone_contacto_opt', null=True)
    sim_number_opt = models.CharField(max_length=255, db_column='sim_numb_opt', null=True)
    sim_serial_opt = models.CharField(max_length=255, null=True)
    mac_number = models.CharField(max_length=255, db_column='mac_numb', null=True)
    device_serial_opt = models.CharField(max_length=255, null=True)

    contact_person = models.CharField(max_length=255, null=True, db_column='pessoa_contacto')
    phone_contact = models.CharField(max_length=255, null=True, db_column='telefone_contacto')

    province = models.ForeignKey(Province)
    district = models.ForeignKey(District)
