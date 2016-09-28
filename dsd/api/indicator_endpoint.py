from datetime import datetime

import random
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
            start_date, end_date, ous = check_params(request.GET)

            start_week = get_isoweek(start_date)
            end_week = get_isoweek(end_date)
            facilities = ous.split(':')

            response = {}
            for facility in facilities:
                response.update({facility: [get_indicator_info() for _ in range(0, end_week - start_week + 1)]})

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
    return {'syncStatus': get_random_status(),
            'syncTime': {
                'time': datetime.now(),
                'status': get_random_status()
            },
            'ODKVersion': get_random_version()}


def get_random_status():
    return random.randint(-1, 1)


def get_random_version():
    return 'v1.%s' % random.randint(1, 35)
