from datetime import datetime

import random
from django.db import connections
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from dsd.exceptions.illegal_arguments_exception import IllegalArgumentException

START_DATE = 'startDate'
END_DATE = 'endDate'
OUS = 'organisationUnits'


@csrf_exempt
def indicator_endpoint(request):
    try:
        if request.method == 'GET':
            # start_date, end_date, ous = check_params(request.GET)

            # start_week = get_isoweek(start_date)
            # end_week = get_isoweek(end_date)
            # facilities = ous.split(':')

            response = {}
            # for facility in facilities:
            #     response.update({facility: [get_indicator_info() for _ in range(0, end_week - start_week + 1)]})


            with connections['chai'].cursor() as cursor:
                cursor.execute('SELECT f.facility_name, '
                               '(CASE WHEN "CASOS_COLERA" = -1 OR "CASOS_COLERA" IS NULL '
                               'OR "CASOS_DIARREIA_0_4" = -1 OR "CASOS_DIARREIA_0_4" IS NULL '
                               'OR "CASOS_DIARREIA_15" = -1 OR "CASOS_DIARREIA_15" IS NULL '
                               'OR "CASOS_DIARREIA_5_14" = -1 OR "CASOS_DIARREIA_5_14" IS NULL '
                               'OR "CASOS_DISENTERIA" = -1 OR "CASOS_DISENTERIA" IS NULL '
                               'OR "CASOS_MALARIA_CLINICA_0_4" = -1 OR "CASOS_MALARIA_CLINICA_0_4" IS NULL '
                               'OR "CASOS_MALARIA_CLINICA_5" = -1 OR "CASOS_MALARIA_CLINICA_5" IS NULL '
                               'OR "CASOS_MALARIA_CONFIRMADA_0_4" = -1 OR "CASOS_MALARIA_CONFIRMADA_0_4" IS NULL '
                               'OR "CASOS_MALARIA_CONFIRMADA_5" = -1 OR "CASOS_MALARIA_CONFIRMADA_5" IS NULL '
                               'OR "CASOS_MENINGITE_0_4" = -1 OR "CASOS_MENINGITE_0_4" IS NULL '
                               'OR "CASOS_MENINGITE_5" = -1 OR "CASOS_MENINGITE_5" IS NULL '
                               'OR "CASOS_PESTE" = -1 OR "CASOS_PESTE" IS NULL '
                               'OR "CASOS_PFA" = -1 OR "CASOS_PFA" IS NULL '
                               'OR "CASOS_RAIVA" = -1 OR "CASOS_RAIVA" IS NULL '
                               'OR "CASOS_SARAMPO_24" = -1 OR "CASOS_SARAMPO_24" IS NULL '
                               'OR "CASOS_SARAMPO_9" = -1 OR "CASOS_SARAMPO_9" IS NULL '
                               'OR "CASOS_SARAMPO_NV_9_23" = -1 OR "CASOS_SARAMPO_NV_9_23" IS NULL '
                               'OR "CASOS_SARAMPO_V_9_23" = -1 OR "CASOS_SARAMPO_V_9_23" IS NULL '
                               'OR "CASOS_TETANO" = -1 OR "CASOS_TETANO" IS NULL '
                               'OR "OBITOS_COLERA" = 1 OR "OBITOS_COLERA" IS NULL '
                               'OR "OBITOS_DIARREIA_0_4" = -1 OR "OBITOS_DIARREIA_0_4" IS NULL '
                               'OR "OBITOS_DIARREIA_15" = -1 OR "OBITOS_DIARREIA_15" IS NULL '
                               'OR "OBITOS_DIARREIA_5_14" = -1 OR "OBITOS_DIARREIA_5_14" IS NULL '
                               'OR "OBITOS_DISENTERIA" = -1 OR "OBITOS_DISENTERIA" IS NULL '
                               'OR "OBITOS_MALARIA_CLINICA_0_4" = -1 OR "OBITOS_MALARIA_CLINICA_0_4" IS NULL '
                               'OR "OBITOS_MALARIA_CLINICA_5" = -1 OR "OBITOS_MALARIA_CLINICA_5" IS NULL '
                               'OR "OBITOS_MALARIA_CONFIRMADA_0_4" = -1 OR "OBITOS_MALARIA_CONFIRMADA_0_4" IS NULL '
                               'OR "OBITOS_MALARIA_CONFIRMADA_5" = -1 OR "OBITOS_MALARIA_CONFIRMADA_5" IS NULL '
                               'OR "OBITOS_MENINGITE_0_4" = -1 OR "OBITOS_MENINGITE_0_4" IS NULL '
                               'OR "OBITOS_MENINGITE_5" = -1 OR "OBITOS_MENINGITE_5" IS NULL '
                               'OR "OBITOS_PESTE" = -1 OR "OBITOS_PESTE" IS NULL '
                               'OR "OBITOS_PFA" = -1 OR "OBITOS_PFA" IS NULL '
                               'OR "OBITOS_RAIVA" = -1 OR "OBITOS_RAIVA" IS NULL '
                               'OR "OBITOS_SARAMPO_24" = -1 OR "OBITOS_SARAMPO_24" IS NULL '
                               'OR "OBITOS_SARAMPO_9" = -1 OR "OBITOS_SARAMPO_9" IS NULL '
                               'OR "OBITOS_SARAMPO_NV_9_23" = -1 OR "OBITOS_SARAMPO_NV_9_23" IS NULL '
                               'OR "OBITOS_SARAMPO_V_9_23" = -1 OR "OBITOS_SARAMPO_V_9_23" IS NULL '
                               'OR "OBITOS_TETANO" = -1 OR "OBITOS_TETANO" IS NULL '
                               'THEN \'incompleted\' '
                               'ELSE \'completed\' END) AS syncStatus, '
                               '(CASE WHEN date_part(\'week\', b."_SUBMISSION_DATE") < b."BES_NUMBER" '
                               'OR (date_part(\'week\', b."_SUBMISSION_DATE") = b."BES_NUMBER" AND date_part(\'isodow\', b."_SUBMISSION_DATE") < 7) THEN \'Early\' '
                               'WHEN date_part(\'week\', b."_SUBMISSION_DATE") > b."BES_NUMBER" + 1 OR '
                               '(date_part(\'week\', b."_SUBMISSION_DATE") = b."BES_NUMBER" + 1 AND date_part(\'isodow\', b."_SUBMISSION_DATE") > 2) THEN \'Later\' '
                               'ELSE \'Normal\' END) AS freshness, '
                               'b."_SUBMISSION_DATE", b."BES_NUMBER", date_part(\'week\', b."_SUBMISSION_DATE") as weekOfYear, '
                               'date_part(\'isodow\', b."_SUBMISSION_DATE") AS dayOfWeek '
                               'FROM facilities f INNER JOIN "BES_MIDDLEWARE_CORE" b ON f.device_serial = b."DEVICEID" '
                               'WHERE f.facility_name = \'CENTRO DE SAUDE DE NGOLHOSA\' AND b."BES_YEAR" = \'2016-01-01\' AND b."BES_NUMBER" = 33 '
                               'ORDER BY b."_SUBMISSION_DATE" DESC')
                row = cursor.fetchall()

                print(row)

            return JsonResponse(response)
    except IllegalArgumentException as e:
        return HttpResponse(status=e.status_code, content=e.error_message)
    except Exception as e:
        return HttpResponse(status=500, content='Error: %s' % e)


def check_params(params):
    start_date = params.get(START_DATE)
    end_date = params.get(END_DATE)
    ous = params.get(OUS)

    if not (start_date and end_date and ous):
        raise IllegalArgumentException(message='Check the url.')

    return start_date, end_date, ous


def get_isoweek(date):
    return datetime.fromtimestamp(float(date) / 1000).isocalendar()[1]


def get_indicator_info():
    return {'syncStatus': None,
            'syncTime': {
                'time': None,
                'status': None
            },
            'ODKVersion': None}


def get_random_status():
    return random.randint(-1, 1)


def get_random_version():
    return 'v1.%s' % random.randint(1, 35)
