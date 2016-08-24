from django.db import models

from dsd.models import District
from dsd.models import Province


class Facility(models.Model):
    class Meta:
        app_label = 'dsd'
        db_table = 'facilities'

    facility_name = models.CharField(max_length=255, unique=True)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    code_us = models.CharField(max_length=255)
    sorting_us = models.CharField(max_length=255, db_column='classificacao_us')
    level_us = models.CharField(max_length=255, db_column='nivel_us')
    ugly_us = models.CharField(max_length=255, db_column='fea_us')
    province_capital_dist = models.IntegerField(null=True)
    device_serial = models.CharField(max_length=255)
    sim_number = models.CharField(max_length=255, unique=True, db_column='sim_numb')
    sim_serial = models.CharField(max_length=255, unique=True)
    device_number = models.CharField(max_length=255, db_column='device_numb')
    state = models.IntegerField(db_column='estado')

    person_contact_opt = models.CharField(max_length=255, db_column='pessoa_contacto_opt')
    phone_contact_opt = models.CharField(max_length=255, db_column='telefone_contacto_opt')
    sim_number_opt = models.CharField(max_length=255, unique=True, db_column='sim_numb_opt')
    sim_serial_opt = models.CharField(max_length=255, unique=True)
    mac_number = models.CharField(max_length=255, db_column='mac_numb')
    device_serial_opt = models.CharField(max_length=255)

    province = models.ForeignKey(Province)
    district = models.ForeignKey(District)
