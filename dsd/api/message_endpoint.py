from datetime import datetime
from django.db import connections
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status

from dsd.exceptions.illegal_arguments_exception import IllegalArgumentException
from dsd.services.message_service import START_DAY, END_DAY, LOCATION, fetch_ou_id_by_ou_uid, sql_get_moh_data, \
    sql_get_data_by_filter, sql_find_location_name


@csrf_exempt
@api_view(['GET', ])
@renderer_classes((JSONRenderer,))
def data_message_endpoint(request):
    try:
        start, end, ou = check_params(request.GET)
        location_level, location_id = fetch_ou_id_by_ou_uid(ou)
        start_day = datetime.fromtimestamp(float(start) / 1000).strftime('%Y-%m-%d')
        end_day = datetime.fromtimestamp(float(end) / 1000).strftime('%Y-%m-%d')

        response = []
        with connections['chai'].cursor() as cursor:
            if location_level == 'COUNTRY':
                cursor.execute(sql_get_moh_data(start_day, end_day))
                rows = cursor.fetchall()

            else:
                cursor.execute(sql_get_data_by_filter(location_level, location_id, start_day, end_day))
                rows = cursor.fetchall()

            for row in rows:
                response.append(get_message_info(row))

        return Response(response, status=status.HTTP_200_OK)

    except IllegalArgumentException as e:
        return Response(e.error_message, status=e.status_code)

    except Exception as e:
        return Response('Error: %s' % e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_message_info(row):
    province = row[0] if row[0] else ' '
    district = row[1] if row[1] else ' '
    facility = row[2] if row[2] else ' '
    created = row[4].strftime('%Y-%m-%d %H:%M:%S') if row[4] else ' '
    submitted = row[5].strftime('%Y-%m-%d %H:%M:%S') if row[5] else ' '

    return {'province': province,
            'district': district,
            'facility': facility,
            'message': row[3],
            'created': created,
            'submitted': submitted}


def check_params(params):
    start_day = params.get(START_DAY)
    end_day = params.get(END_DAY)
    ou = params.get(LOCATION)

    if not (start_day and end_day and ou):
        raise IllegalArgumentException(message='%s, %s, %s are mandatory.' % (START_DAY, END_DAY, LOCATION))

    start = get_isocalendar(start_day)
    end = get_isocalendar(end_day)

    if start > end:
        raise IllegalArgumentException(message='%s must less than %s.' % (START_DAY, END_DAY))

    return start_day, end_day, ou


def get_isocalendar(date):
    return datetime.fromtimestamp(float(date) / 1000).isocalendar()
