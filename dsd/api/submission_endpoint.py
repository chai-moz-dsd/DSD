from datetime import datetime
from django.db import connections
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status

from dsd.exceptions.illegal_arguments_exception import IllegalArgumentException
from dsd.services.submission_service import START_DAY, END_DAY, LOCATION, INDEX_PAGE, fetch_ou_id_by_ou_uid, \
    sql_get_total_number_no_location, sql_get_total_number, sql_get_details_no_location, sql_get_details


@csrf_exempt
@api_view(['GET', ])
@renderer_classes((JSONRenderer,))
def data_submission_endpoint(request):
    try:
        start, end, ou, page_index = check_params(request.GET)
        location_level, location_id = fetch_ou_id_by_ou_uid(ou)
        start_day = datetime.fromtimestamp(float(start) / 1000).strftime('%Y-%m-%d')
        end_day = datetime.fromtimestamp(float(end) / 1000).strftime('%Y-%m-%d')

        response = []
        if not page_index:
            total_number = select_total_count(location_level, location_id, start_day, end_day)
            response = total_number
        else:
            details = select_details(location_level, location_id, start_day, end_day, page_index)
            for detail in details:
                response.append(get_submission_info(detail))

        return Response(response, status=status.HTTP_200_OK)

    except IllegalArgumentException as e:
        return Response(e.error_message, status=e.status_code)

    except Exception as e:
        return Response('Error: %s' % e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# refactor
def get_submission_info(detail):
    facility = detail[0] if detail[0] else ' '
    district = detail[1] if detail[1] else ' '
    province = detail[2] if detail[2] else ' '
    week_end_date = detail[3].strftime('%Y-%m-%d') if detail[3] else ' '
    week = ('W' + str(detail[4])) if detail[4] else ' '
    cases_colera = detail[5] if detail[5] != -1 else '-'
    deaths_colera = detail[6] if detail[6] != -1 else '-'
    cases_dysentery = detail[7] if detail[7] != -1 else '-'
    deaths_dysentery = detail[8] if detail[8] != -1 else '-'
    cases_plague = detail[9] if detail[9] != -1 else '-'
    deaths_plague = detail[10] if detail[10] != -1 else '-'
    cases_tetanus = detail[11] if detail[11] != -1 else '-'
    deaths_tetanus = detail[12] if detail[12] != -1 else '-'
    cases_pfa = detail[13] if detail[13] != -1 else '-'
    deaths_pfa = detail[14] if detail[14] != -1 else '-'
    cases_rabies = detail[15] if detail[15] != -1 else '-'
    deaths_rabies = detail[16] if detail[16] != -1 else '-'
    cases_diarrhea_04 = detail[17] if detail[17] != -1 else '-'
    deaths_diarrhea_04 = detail[18] if detail[18] != -1 else '-'
    cases_diarrhea_5_14 = detail[19] if detail[19] != -1 else '-'
    deaths_diarrhea_5_14 = detail[20] if detail[20] != -1 else '-'
    cases_diarrhea_15 = detail[21] if detail[21] != -1 else '-'
    deaths_diarrhea_15 = detail[22] if detail[22] != -1 else '-'
    cases_malaria_clinic_0_4 = detail[23] if detail[23] != -1 else '-'
    deaths_malaria_clinic_0_4 = detail[24] if detail[24] != -1 else '-'
    cases_malaria_clinic_5 = detail[25] if detail[25] != -1 else '-'
    deaths_malaria_clinic_5 = detail[26] if detail[26] != -1 else '-'
    cases_malaria_confirmed_0_4 = detail[27] if detail[27] != -1 else '-'
    deaths_malaria_confirmed_0_4 = detail[28] if detail[28] != -1 else '-'
    cases_malaria_confirmed_5 = detail[29] if detail[29] != -1 else '-'
    deaths_malaria_confirmed_5 = detail[30] if detail[30] != -1 else '-'
    cases_meningitis_0_4 = detail[31] if detail[31] != -1 else '-'
    deaths_meningitis_04 = detail[32] if detail[32] != -1 else '-'
    cases_meningitis_5 = detail[33] if detail[33] != -1 else '-'
    deaths_meningitis_5 = detail[34] if detail[34] != -1 else '-'
    cases_measles_9 = detail[35] if detail[35] != -1 else '-'
    deaths_measles_9 = detail[36] if detail[36] != -1 else '-'
    cases_nv_measles = detail[37] if detail[37] != -1 else '-'
    deaths_measles_nv = detail[38] if detail[38] != -1 else '-'
    cases_measles_v9_23 = detail[39] if detail[39] != -1 else '-'
    deaths_measles_v_9_23 = detail[40] if detail[40] != -1 else '-'
    cases_measles_24 = detail[41] if detail[41] != -1 else '-'
    deaths_measles_24 = detail[42] if detail[42] != -1 else '-'
    skippable_open_field = detail[43] if detail[43] else ' '

    return {'facility': facility,
            'district': district,
            'province': province,
            'week_end_date': week_end_date,
            'week': week,
            'cases_colera': cases_colera,
            'deaths_colera': deaths_colera,
            'cases_dysentery': cases_dysentery,
            'deaths_dysentery': deaths_dysentery,
            'cases_plague': cases_plague,
            'deaths_plague': deaths_plague,
            'cases_tetanus': cases_tetanus,
            'deaths_tetanus': deaths_tetanus,
            'cases_pfa': cases_pfa,
            'deaths_pfa': deaths_pfa,
            'cases_rabies': cases_rabies,
            'deaths_rabies': deaths_rabies,
            'cases_diarrhea_04': cases_diarrhea_04,
            'deaths_diarrhea_04': deaths_diarrhea_04,
            'cases_diarrhea_5_14': cases_diarrhea_5_14,
            'deaths_diarrhea_5_14': deaths_diarrhea_5_14,
            'cases_diarrhea_15': cases_diarrhea_15,
            'deaths_diarrhea_15': deaths_diarrhea_15,
            'cases_malaria_clinic_0_4': cases_malaria_clinic_0_4,
            'deaths_malaria_clinic_0_4': deaths_malaria_clinic_0_4,
            'cases_malaria_clinic_5': cases_malaria_clinic_5,
            'deaths_malaria_clinic_5': deaths_malaria_clinic_5,
            'cases_malaria_confirmed_0_4': cases_malaria_confirmed_0_4,
            'deaths_malaria_confirmed_0_4': deaths_malaria_confirmed_0_4,
            'cases_malaria_confirmed_5': cases_malaria_confirmed_5,
            'deaths_malaria_confirmed_5': deaths_malaria_confirmed_5,
            'cases_meningitis_0_4': cases_meningitis_0_4,
            'deaths_meningitis_04': deaths_meningitis_04,
            'cases_meningitis_5': cases_meningitis_5,
            'deaths_meningitis_5': deaths_meningitis_5,
            'cases_measles_9': cases_measles_9,
            'deaths_measles_9': deaths_measles_9,
            'cases_nv_measles': cases_nv_measles,
            'deaths_measles_nv': deaths_measles_nv,
            'cases_measles_v9_23': cases_measles_v9_23,
            'deaths_measles_v_9_23': deaths_measles_v_9_23,
            'cases_measles_24': cases_measles_24,
            'deaths_measles_24': deaths_measles_24,
            'skippable_open_field': skippable_open_field
            }


def select_total_count(location_level, location_id, start_day, end_day):
    with connections['default'].cursor() as cursor:
        if location_level == 'COUNTRY':
            cursor.execute(sql_get_total_number_no_location(start_day, end_day))
            rows = cursor.fetchall()

        else:
            cursor.execute(sql_get_total_number(location_level, location_id, start_day, end_day))
            rows = cursor.fetchall()
    cursor.close()

    return rows[0][0]


def select_details(location_level, location_id, start_day, end_day, page_index):
    with connections['default'].cursor() as cursor:
        if location_level == 'COUNTRY':
            cursor.execute(sql_get_details_no_location(start_day, end_day, page_index))
            rows = cursor.fetchall()

        else:
            cursor.execute(sql_get_details(location_level, location_id, start_day, end_day, page_index))
            rows = cursor.fetchall()
    cursor.close()

    return rows


def check_params(params):
    start_day = params.get(START_DAY)
    end_day = params.get(END_DAY)
    ou = params.get(LOCATION)
    page_index = params.get(INDEX_PAGE)

    if not (start_day and end_day and ou):
        raise IllegalArgumentException(message='%s, %s, %s are mandatory.' % (START_DAY, END_DAY, LOCATION))

    start = get_iso_calendar(start_day)
    end = get_iso_calendar(end_day)

    if start > end:
        raise IllegalArgumentException(message='%s must less than %s.' % (START_DAY, END_DAY))

    return start_day, end_day, ou, page_index


def get_iso_calendar(date):
    return datetime.fromtimestamp(float(date) / 1000).isocalendar()
