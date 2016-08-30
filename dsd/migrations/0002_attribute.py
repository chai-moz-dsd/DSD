# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-29 09:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsd', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255)),
                ('valueType', models.CharField(max_length=255)),
                ('orgUnitAttr', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'attributes',
            },
        ),
    ]
