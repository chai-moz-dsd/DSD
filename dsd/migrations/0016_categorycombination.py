# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-02 03:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsd', '0015_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryCombination',
            fields=[
                ('id', models.CharField(max_length=11, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(default='', max_length=255)),
                ('categories', models.ManyToManyField(to='dsd.Category')),
            ],
        ),
    ]