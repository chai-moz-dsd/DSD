from datetime import datetime

import random
from django.db import connections
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from dsd.exceptions.illegal_arguments_exception import IllegalArgumentException
from dsd.services.indicator_service import START_DATE, END_DATE, OUS, get_sql_command, MAX_WEEK

SYNC_STATUS = {'Completed': 1, 'Incompleted': 0, 'Not_submitted': -1}
FRESHNESS = {'Early': 1, 'Normal': 0, 'Later': -1}


@csrf_exempt
@api_view(['GET', ])
@renderer_classes((JSONRenderer,))
def indicator_endpoint(request):
    try:
        start_date, end_date, ous = check_params(request.GET)

        start = get_isocalendar(start_date)
        end = get_isocalendar(end_date)
        facilities = ous.split(':')

        response = {}
        with connections['chai'].cursor() as cursor:
            cursor.execute(get_sql_command(facilities, start, end))
            rows = cursor.fetchall()
            rows = fill_row(rows, facilities, start, end)

            for facility in facilities:
                response.update({facility: [get_indicator_info(row) for row in rows]})

            response.update({})

        return Response(response, status=status.HTTP_200_OK)
    except IllegalArgumentException as e:
        return Response(e.error_message, status=e.status_code)
    except Exception as e:
        return Response('Error: %s' % e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def check_params(params):
    start_date = params.get(START_DATE)
    end_date = params.get(END_DATE)
    ous = params.get(OUS)

    if not (start_date and end_date and ous):
        raise IllegalArgumentException(message='%s, %s, %s are mandatory.' % (START_DATE, END_DATE, OUS))

    start = get_isocalendar(start_date)
    end = get_isocalendar(end_date)

    if start > end:
        raise IllegalArgumentException(message='%s must less than %s.' % (START_DATE, END_DATE))

    return start_date, end_date, ous


def get_isocalendar(date):
    return datetime.fromtimestamp(float(date) / 1000).isocalendar()


def get_indicator_info(element):
    sync_status = SYNC_STATUS.get(element[1], None)
    freshness = FRESHNESS.get(element[2], None)
    submission_time = element[3]
    version = 'v1.1'

    return {'syncStatus': sync_status,
            'syncTime': {
                'time': submission_time,
                'status': freshness
            },
            'ODKVersion': version}


def get_random_status():
    return random.randint(-1, 1)


def get_random_version():
    return 'v1.%s' % random.randint(1, 35)


def fill_row(rows, facilities, start, end):
    def get_empty_row(name):
        return (name, 'Not_submitted', None, None, None)

    def get_row(inner_facility, inner_year, inner_week):
        index = -1

        for i, row in enumerate(rows):
            if row[0] == inner_facility and row[4] == datetime(inner_year, 1, 1, 0, 0) and row[5] == inner_week:
                index = i

        if index != -1:
            return rows[index]
        else:
            return get_empty_row(inner_facility)

    start_year = start[0]
    start_week = start[1]
    end_year = end[0]
    end_week = end[1]

    res = []
    for facility in facilities:
        if start_year == end_year:
            for week in range(start_week, end_week + 1):
                print('week', week)
                res.append(get_row(facility, start_year, week))
        else:
            for week in range(start_week, MAX_WEEK + 1):
                res.append(get_row(facility, start_year, week))
            for week in range(1, end_week + 1):
                res.append(get_row(facility, end_year, week))

    return res
