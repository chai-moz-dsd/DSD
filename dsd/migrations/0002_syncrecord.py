# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-30 01:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsd', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SyncRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_sync_time', models.DateTimeField()),
            ],
        ),
    ]
