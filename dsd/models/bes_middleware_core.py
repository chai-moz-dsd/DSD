from django.db import models


class BesMiddlewareCore(models.Model):
    class Meta:
        app_label = 'dsd'
        db_table = 'BES_MIDDLEWARE_CORE'

    uri = models.CharField(max_length=80, unique=True, primary_key=True)
    creator_uri_user = models.CharField(max_length=80)
    creation_date = models.DateTimeField()
    last_update_uri_user = models.CharField(max_length=255, null=True)
    last_update_date = models.DateTimeField()
    model_version = models.IntegerField(null=True)
    ui_version = models.IntegerField(null=True)
    is_complete = models.NullBooleanField(null=True)
    submission_date = models.DateTimeField(null=True)
    marked_as_complete_date = models.DateTimeField(null=True)
    sim_serial_test_output = models.CharField(max_length=255, null=True)
    note_intro = models.CharField(max_length=255, null=True)
    bes_year = models.DateTimeField(null=True)
    deaths_diarrhea_04 = models.IntegerField(null=True)
    deaths_diarrhea_15 = models.IntegerField(null=True)
    deaths_measles_nv = models.IntegerField(null=True)
    deaths_meningitis_5 = models.IntegerField(null=True)
    cases_diarrhea_04 = models.IntegerField(null=True)
    deaths_meningitis_04 = models.IntegerField(null=True)
    device_id_test_output = models.CharField(max_length=255, null=True)
    date_week_end = models.DateTimeField(null=True)
    note_measles = models.CharField(max_length=255, null=True)
    end_test_output = models.CharField(max_length=255, null=True)
    metadata_note = models.CharField(max_length=255, null=True)
    note_diarrhea = models.CharField(max_length=255, null=True)
    cases_nv_measles = models.IntegerField(null=True)
    cases_anger = models.IntegerField(null=True)
    note_malaria = models.CharField(max_length=255, null=True)
    device_id = models.CharField(max_length=255, null=True)
    deaths_measles_24 = models.IntegerField(null=True)
    note_anger = models.CharField(max_length=255, null=True)
    deaths_diarrhea_5_14 = models.IntegerField(null=True)
    skippable_open_field = models.CharField(max_length=255, null=True)
    cases_meningitis_0_4 = models.IntegerField(null=True)
    cases_cholera = models.IntegerField(null=True)
    end = models.DateTimeField(null=True)
    cases_tetanus = models.IntegerField(null=True)
    cases_diarrhea_5_14 = models.IntegerField(null=True)
    note_meningitis = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)
    bes_number = models.IntegerField(null=True)
    deaths_anger = models.IntegerField(null=True)
    start_test_output = models.CharField(max_length=255, null=True)
    skip_open_field = models.CharField(max_length=255, null=True)
    note_pfa = models.CharField(max_length=255, null=True)
    cases_malaria_5 = models.IntegerField(null=True)
    meta_instance_id = models.CharField(max_length=255, null=True)
    cases_measles_24 = models.IntegerField(null=True)
    sim_serial = models.CharField(max_length=255, null=True)
    cases_measles_9 = models.IntegerField(null=True)
    phone_number_test_output = models.CharField(max_length=255, null=True)
    date_week_start = models.DateTimeField(null=True)
    cases_pfa = models.IntegerField(null=True)
    today = models.DateTimeField(null=True)
    deaths_plague = models.IntegerField(null=True)
    cases_meningitis_5 = models.IntegerField(null=True)
    cases_dysentery = models.IntegerField(null=True)
    cases_measles_v9_23 = models.IntegerField(null=True)
    deaths_malaria_5 = models.IntegerField(null=True)
    deaths_dysentery = models.IntegerField(null=True)
    cases_diarrhea_15 = models.IntegerField(null=True)
    note_plague = models.CharField(max_length=255, null=True)
    deaths_pfa = models.IntegerField(null=True)
    note_tetanus = models.CharField(max_length=255, null=True)
    note_dysentery = models.CharField(max_length=255, null=True)
    deaths_malaria_0_4 = models.IntegerField(null=True)
    cases_malaria_0_4 = models.IntegerField(null=True)
    deaths_tetanus = models.IntegerField(null=True)
    start = models.DateTimeField(null=True)
    deaths_measles_v_9_23 = models.IntegerField(null=True)
    deaths_cholera = models.IntegerField(null=True)
    note_cholera = models.CharField(max_length=255, null=True)
    deaths_measles_9 = models.IntegerField(null=True)
    cases_plague = models.IntegerField(null=True)
    today_test_output = models.CharField(max_length=255, null=True)
    cases_clinic_malaria_0_4 = models.IntegerField(default=0, null=True)
    cases_clinic_malaria_5 = models.IntegerField(default=0, null=True)
    deaths_clinic_malaria_0_4 = models.IntegerField(default=0, null=True)
    deaths_clinic_malaria_5 = models.IntegerField(default=0, null=True)
