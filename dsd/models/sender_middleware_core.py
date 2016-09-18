from django.db import models


class SenderMiddlewareCore(models.Model):
    class Meta:
        app_label = 'dsd'

    uri = models.CharField(max_length=80, unique=True, primary_key=True)
    creator_uri_user = models.CharField(max_length=80)
    creation_date = models.DateTimeField()
    middleware_created_date = models.DateTimeField()
    middleware_updated_date = models.DateTimeField()
    last_update_uri_user = models.CharField(max_length=80, null=True)
    last_update_date = models.DateTimeField()
    model_version = models.IntegerField(null=True)
    ui_version = models.IntegerField(null=True)
    is_complete = models.NullBooleanField(null=True)
    submission_date = models.DateTimeField(null=True)
    marked_as_complete_date = models.DateTimeField(null=True)
    device_id_test_output = models.CharField(max_length=255, null=True)
    end_test_output = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)
    today = models.DateTimeField(null=True)
    start_test_output = models.CharField(max_length=255, null=True)
    sim_serial_test_output = models.CharField(max_length=255, null=True)
    metadata_note = models.CharField(max_length=255, null=True)
    note_intro = models.CharField(max_length=255, null=True)
    note_description = models.CharField(max_length=255, null=True)
    meta_instance_id = models.CharField(max_length=255, null=True)
    sim_serial = models.CharField(max_length=255, null=True)
    device_id = models.CharField(max_length=255, null=True)
    open_field = models.CharField(max_length=255, null=True)
    phone_number_test_output = models.CharField(max_length=255, null=True)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    today_test_output = models.CharField(max_length=255, null=True)
