from django.db import models


class BesVersionCore(models.Model):
    class Meta:
        app_label = 'dsd'
        db_table = 'BES_VERSAO1_0_CORE'

    uri = models.CharField(max_length=80, db_column='_URI', unique=True)
    creator_uri_user = models.CharField(max_length=80, db_column='_CREATOR_URI_USER')
    creation_date = models.DateTimeField(db_column='_CREATION_DATE')
    last_update_uri_user = models.CharField(max_length=255, db_column='_LAST_UPDATE_URI_USER', null=True)
    last_update_date = models.DateTimeField(db_column='_LAST_UPDATE_DATE')
    model_version = models.IntegerField(db_column='_MODEL_VERSION', null=True)
    ui_version = models.IntegerField(db_column='_UI_VERSION', null=True)
    is_complete = models.NullBooleanField(db_column='descricao', null=True)
    submission_date = models.DateTimeField(db_column='_SUBMISSION_DATE', null=True)
    marked_as_complete_date = models.DateTimeField(db_column='_MARKED_AS_COMPLETE_DATE', null=True)
    sim_serial_test_output = models.CharField(max_length=255, db_column='SIMSERIAL_TEST_OUTPUT', null=True)
    note_intro = models.CharField(max_length=255, db_column='NOTE_INTRO', null=True)
    bes_year = models.DateTimeField(db_column='BES_YEAR', null=True)
    diarrhea_deaths04 = models.IntegerField(db_column='OBITOS_DIARREIA_0_4', null=True)
    diarrhea_deaths15 = models.IntegerField(db_column='OBITOS_DIARREIA_15', null=True)
    measles_deaths_nv = models.IntegerField(db_column='OBITOS_SARAMPO_NV_9_23', null=True)
    meningitis_deaths5 = models.IntegerField(db_column='OBITOS_MENINGITE_5', null=True)
    cases_diarrhea_04 = models.IntegerField(db_column='CASOS_DIARREIA_0_4', null=True)
    meningitis_deaths04 = models.IntegerField(db_column='OBITOS_MENINGITE_0_4', null=True)
    device_id_test_output = models.CharField(max_length=255, db_column='DEVICEID_TEST_OUTPUT', null=True)
    date_week_end = models.DateTimeField(db_column='DATE_WEEK_END', null=True)
    description = models.CharField(max_length=255, db_column='NOTE_SARAMPO', null=True)
    end_test_output = models.CharField(max_length=255, db_column='END_TEST_OUTPUT', null=True)
    metadata_note = models.CharField(max_length=255, db_column='METADATA_NOTE', null=True)
    note_diarrhea = models.CharField(max_length=255, db_column='NOTE_DIARREIA', null=True)
    cases_nv_measles = models.IntegerField(db_column='CASOS_SARAMPO_NV_9_23', null=True)
    cases_anger = models.IntegerField(db_column='CASOS_RAIVA', null=True)
    note_malaria = models.CharField(max_length=255, db_column='NOTE_MALARIA', null=True)
    device_id = models.CharField(max_length=255, db_column='DEVICEID', null=True)
    deaths_measles_24 = models.IntegerField(db_column='OBITOS_SARAMPO_24', null=True)
    note_raiva = models.CharField(max_length=255, db_column='NOTE_RAIVA', null=True)
    deaths_diarrhea_5_14 = models.IntegerField(db_column='OBITOS_DIARREIA_5_14', null=True)
    skippable_open_field = models.CharField(max_length=255, db_column='SKIPABLE_CAMPO_ABERTO', null=True)
    cases_meningitis_0_4 = models.IntegerField(db_column='CASOS_MENINGITE_0_4', null=True)
    cases_colera = models.IntegerField(db_column='CASOS_COLERA', null=True)
    end = models.DateTimeField(db_column='END', null=True)
    cases_tetanus = models.IntegerField(db_column='CASOS_TETANO', null=True)
    cases_diarrhea_5_14 = models.IntegerField(db_column='CASOS_DIARREIA_5_14', null=True)
    note_meningitis = models.CharField(max_length=255, db_column='NOTE_MENINGITE', null=True)
    phone_number = models.CharField(max_length=255, db_column='PHONENUMBER', null=True)
    bes_number = models.IntegerField(db_column='BES_NUMBER', null=True)
    deaths_anger = models.IntegerField(db_column='OBITOS_RAIVA', null=True)
    start_test_output = models.CharField(max_length=255, db_column='START_TEST_OUTPUT', null=True)
    skip_open_field = models.CharField(max_length=255, db_column='SKIP_CAMPO_ABERTO', null=True)
    note_pfa = models.CharField(max_length=255, db_column='NOTE_PFA', null=True)
    cases_malaria_5 = models.IntegerField(db_column='CASOS_MALARIA_5', null=True)
    meta_instance_id = models.CharField(max_length=255, db_column='META_INSTANCE_ID', null=True)
    cases_measles_24 = models.IntegerField(db_column='CASOS_SARAMPO_24', null=True)
    sim_serial = models.CharField(max_length=255, db_column='SIMSERIAL', null=True)
    cases_measles_9 = models.IntegerField(db_column='CASOS_SARAMPO_9', null=True)
    phone_number_test_output = models.CharField(max_length=255, db_column='PHONENUMBER_TEST_OUTPUT', null=True)
    date_week_start = models.DateTimeField(db_column='DATE_WEEK_START', null=True)
    cases_pfa = models.IntegerField(db_column='CASOS_PFA', null=True)
    today = models.DateTimeField(db_column='TODAY', null=True)
    deaths_plague = models.IntegerField(db_column='OBITOS_PESTE', null=True)
    cases_meningitis_5 = models.IntegerField(db_column='CASOS_MENINGITE_5', null=True)
    cases_dysentery = models.IntegerField(db_column='CASOS_DISENTERIA', null=True)
    cases_measles_v9_23 = models.IntegerField(db_column='CASOS_SARAMPO_V_9_23', null=True)
    deaths_malaria_5 = models.IntegerField(db_column='OBITOS_MALARIA_5', null=True)
    deaths_dysentery = models.IntegerField(db_column='OBITOS_DISENTERIA', null=True)
    cases_diarrhea_15 = models.IntegerField(db_column='CASOS_DIARREIA_15', null=True)
    note_plague = models.CharField(max_length=255, db_column='NOTE_PESTE', null=True)
    deaths_pfa = models.IntegerField(db_column='OBITOS_PFA', null=True)
    note_tetanus = models.CharField(max_length=255, db_column='NOTE_TETANO', null=True)
    note_dysentery = models.CharField(max_length=255, db_column='NOTE_DISENTERIA', null=True)
    deaths_malaria_0_4 = models.IntegerField(db_column='OBITOS_MALARIA_0_4', null=True)
    cases_malaria_0_4 = models.IntegerField(db_column='CASOS_MALARIA_0_4', null=True)
    deaths_tetanus = models.IntegerField(db_column='OBITOS_TETANO', null=True)
    start = models.DateTimeField(db_column='START', null=True)
    deaths_measles_v_9_23 = models.IntegerField(db_column='OBITOS_SARAMPO_V_9_23', null=True)
    deaths_colera = models.IntegerField(db_column='OBITOS_COLERA', null=True)
    note_colera = models.CharField(max_length=255, db_column='NOTE_COLERA', null=True)
    deaths_measles_9 = models.IntegerField(db_column='OBITOS_SARAMPO_9', null=True)
    cases_plague = models.IntegerField(db_column='CASOS_PESTE', null=True)
    today_test_output = models.CharField(max_length=255, db_column='TODAY_TEST_OUTPUT', null=True)
    cases_clinic_malaria_0_4 = models.IntegerField(default=0, db_column='CASOS_MALARIA_CLINICA_0_4', null=True)
    cases_clinic_malaria_5 = models.IntegerField(default=0, db_column='CASOS_MALARIA_CLINICA_5', null=True)
    deaths_clinic_malaria_0_4 = models.IntegerField(default=0, db_column='OBITOS_MALARIA_CLINICA_0_4', null=True)
    deaths_clinic_malaria_5 = models.IntegerField(default=0, db_column='OBITOS_MALARIA_CLINICA_5', null=True)
