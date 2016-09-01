import uuid
from datetime import datetime

import factory

from dsd.models.bes_middleware_core import BesMiddlewareCore


class BesMiddlewareCoreFactory(factory.DjangoModelFactory):
    class Meta:
        model = BesMiddlewareCore

    uri = 'uuid:%s' % uuid.uuid4()
    creator_uri_user = 'uid:maputo-manhica|%s' % datetime.today()
    creation_date = datetime.today()
    last_update_uri_user = None
    last_update_date = datetime.today()
    model_version = None
    ui_version = None
    is_complete = True
    submission_date = datetime.today()
    marked_as_complete_date = datetime.today()
    sim_serial_test_output = None
    note_intro = None
    bes_year = datetime.today()
    deaths_diarrhea_04 = 0
    deaths_diarrhea_15 = 0
    deaths_measles_nv = 0
    deaths_meningitis_5 = 0
    cases_diarrhea_04 = 1
    deaths_meningitis_04 = 0
    device_id_test_output = None
    date_week_end = datetime.today()
    note_measles = None
    end_test_output = None
    metadata_note = None
    note_diarrhea = None
    cases_nv_measles = 0
    cases_rabies = 0
    note_malaria = None
    device_id = factory.Iterator([356670060315512, 356670060310919, 356670060314465, 356670060310976])
    deaths_measles_24 = 0
    note_rabies = None
    deaths_diarrhea_5_14 = 0
    skippable_open_field = factory.Iterator(
        ['Schistossomiase 03,tinha 05, conjutivite 09 queimadura 01, traumatismo 01 asma 02 , hta 01.', None,
         'Tivemos 2 casos de tinha em pacientes com 2 e 15 anos', None, 'Total de TDR: 37.'])
    cases_meningitis_0_4 = 0
    cases_cholera = 0
    end = datetime.today()
    cases_tetanus = 0
    cases_diarrhea_5_14 = factory.Iterator([2, 3, 0])
    note_meningitis = None
    phone_number = None
    bes_number = factory.Iterator([22, 23, 24])
    deaths_rabies = 0
    start_test_output = None
    skip_open_field = factory.Iterator(['yes', 'no'])
    note_pfa = None
    cases_malaria_5 = factory.Iterator([31, 15, 1, 4, 26, 0, 2, 8, 91, 45])
    meta_instance_id = 'uuid:%s' % uuid.uuid4()
    cases_measles_24 = 0
    sim_serial = factory.Iterator(
        ['8925801150348701867f', '8925801150348674270f', '8925801150348701842f', '8925801150348701768f',
         '8925801150348674791f'])
    cases_measles_9 = 9
    phone_number_test_output = None
    date_week_start = datetime.today()
    cases_pfa = 0
    today = datetime.today()
    deaths_plague = 0
    cases_meningitis_5 = 0
    cases_dysentery = 0
    cases_measles_v9_23 = 0
    deaths_malaria_5 = 0
    deaths_dysentery = 0
    cases_diarrhea_15 = factory.Iterator([7, 0, 1, 2, 6, 9, 16, 4])
    note_plague = None
    deaths_pfa = 0
    note_tetanus = None
    note_dysentery = None
    deaths_malaria_0_4 = 0
    cases_malaria_0_4 = factory.Iterator([10, 8, 0, 2, 11, 1, 39, 18])
    deaths_tetanus = 0
    start = datetime.today()
    deaths_measles_v_9_23 = 0
    deaths_cholera = 0
    note_cholera = None
    deaths_measles_9 = 0
    cases_plague = 0
    today_test_output = None
    cases_clinic_malaria_0_4 = 0
    cases_clinic_malaria_5 = 0
    deaths_clinic_malaria_0_4 = 0
    deaths_clinic_malaria_5 = 0
