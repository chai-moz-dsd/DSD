# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-26 02:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dsd', '0002_auto_20160919_0214'),
    ]

    operations = [
        migrations.RenameField(
            model_name='besmiddlewarecore',
            old_name='cases_clinic_malaria_0_4',
            new_name='cases_malaria_clinic_0_4',
        ),
        migrations.RenameField(
            model_name='besmiddlewarecore',
            old_name='cases_clinic_malaria_5',
            new_name='cases_malaria_clinic_5',
        ),
        migrations.RenameField(
            model_name='besmiddlewarecore',
            old_name='deaths_clinic_malaria_0_4',
            new_name='cases_malaria_confirmed_0_4',
        ),
        migrations.RenameField(
            model_name='besmiddlewarecore',
            old_name='deaths_clinic_malaria_5',
            new_name='cases_malaria_confirmed_5',
        ),
        migrations.RemoveField(
            model_name='besmiddlewarecore',
            name='cases_malaria_0_4',
        ),
        migrations.RemoveField(
            model_name='besmiddlewarecore',
            name='deaths_malaria_0_4',
        ),
        migrations.RemoveField(
            model_name='besmiddlewarecore',
            name='deaths_malaria_5',
        ),
        migrations.AddField(
            model_name='besmiddlewarecore',
            name='deaths_malaria_clinic_0_4',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='besmiddlewarecore',
            name='deaths_malaria_clinic_5',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='besmiddlewarecore',
            name='deaths_malaria_confirmed_5',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='besmiddlewarecore',
            name='creation_date',
            field=models.DateTimeField(db_column='_CREATION_DATE'),
        ),
        migrations.AlterField(
            model_name='besmiddlewarecore',
            name='creator_uri_user',
            field=models.CharField(db_column='_CREATOR_URI_USER', max_length=80),
        ),
        migrations.AlterField(
            model_name='besmiddlewarecore',
            name='last_update_date',
            field=models.DateTimeField(db_column='_LAST_UPDATE_DATE'),
        ),
    ]