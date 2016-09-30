from datetime import datetime

import random
from django.db import connections
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from dsd.exceptions.illegal_arguments_exception import IllegalArgumentException
from dsd.services.indicator_service import START_DATE, END_DATE, OUS, get_sql_command


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
            row = cursor.fetchall()

            print(row)

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
