# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-29 02:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsd', '0003_auto_20160829_0224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasetelement',
            name='data_set_id',
            field=models.CharField(default='2ffaa67f-eb54-4c1b-8c36-8084c639474a', max_length=255),
        ),
        migrations.AlterField(
            model_name='datasetelement',
            name='uid',
            field=models.CharField(default='7a1eb717-fea5-4ef0-8d94-bfd9569e379c', max_length=225),
        ),
        migrations.AlterModelTable(
            name='besversioncore',
            table='BES_MIDDLEWARE_CORE',
        ),
    ]