from django.db import models


class SenderFromVersionCore(models.Model):
    class Meta:
        app_label = 'dsd'
        db_table = 'REMETENTE_FORM_VERSAO1_1_CORE'

    uri = models.CharField(max_length=80, db_column='_URI', unique=True)
    creator_uri_user = models.CharField(max_length=80, db_column='_CREATOR_URI_USER')
    creation_date = models.DateTimeField(db_column='_CREATION_DATE')
    last_update_uri_user = models.CharField(max_length=80, db_column='_LAST_UPDATE_URI_USER', null=True)
    last_update_date = models.DateTimeField(db_column='_LAST_UPDATE_DATE')
    model_version = models.IntegerField(db_column='_MODEL_VERSION', null=True)
    ui_version = models.IntegerField(db_column='_UI_VERSION', null=True)
    is_complete = models.NullBooleanField(db_column='_IS_COMPLETE', null=True)
    submission_date = models.DateTimeField(db_column='_SUBMISSION_DATE', null=True)
    marked_as_complete_date = models.DateTimeField(db_column='_MARKED_AS_COMPLETE_DATE', null=True)
    device_id_test_output = models.CharField(max_length=255, db_column='DEVICEID_TEST_OUTPUT', null=True)
    end_test_output = models.CharField(max_length=255, db_column='END_TEST_OUTPUT', null=True)
    phone_number = models.CharField(max_length=255, db_column='PHONENUMBER', null=True)
    today = models.DateTimeField(db_column='TODAY', null=True)
    start_test_output = models.CharField(max_length=255, db_column='START_TEST_OUTPUT', null=True)
    sim_serial_test_output = models.CharField(max_length=255, db_column='SIMSERIAL_TEST_OUTPUT', null=True)
    metadata_note = models.CharField(max_length=255, db_column='METADATA_NOTE', null=True)
    note_intro = models.CharField(max_length=255, db_column='NOTE_INTRO', null=True)
    note_description = models.CharField(max_length=255, db_column='NOTE_DESCRICAO', null=True)
    meta_instance_id = models.CharField(max_length=255, db_column='META_INSTANCE_ID', null=True)
    sim_serial = models.CharField(max_length=255, db_column='SIMSERIAL', null=True)
    device_id = models.CharField(max_length=255, db_column='DEVICEID', null=True)
    open_field = models.CharField(max_length=255, db_column='CAMPO_ABERTO', null=True)
    phone_number_test_output = models.CharField(max_length=255, db_column='PHONENUMBER_TEST_OUTPUT', null=True)
    start = models.DateTimeField(db_column='START', null=True)
    end = models.DateTimeField(db_column='END', null=True)
    today_test_output = models.CharField(max_length=255, db_column='TODAY_TEST_OUTPUT', null=True)
