# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-21 01:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsd', '0009_auto_20160929_0234'),
    ]

    operations = [
        migrations.AddField(
            model_name='syncrecord',
            name='time_start',
            field=models.DateTimeField(null=True),
        ),
    ]
