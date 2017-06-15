from datetime import datetime
from django.db import connections
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status

from dsd.exceptions.illegal_arguments_exception import IllegalArgumentException
from dsd.services.comments_service import START, END, LOCATION, fetch_ou_id_by_ou_uid, sql_get_moh_data, \
    sql_get_data_by_filter, sql_get_moh_data_one_year, sql_get_data_by_filter_one_year


@csrf_exempt
@api_view(['GET', ])
@renderer_classes((JSONRenderer,))
def data_comments_endpoint(request):
    try:
        start_year, start_week, end_year, end_week, ou = check_params(request.GET)
        location_level, location_id = fetch_ou_id_by_ou_uid(ou)

        print(start_year, start_week, end_year, end_week, ou)
        print(location_level, location_id)

        response = []
        with connections['chai'].cursor() as cursor:
            if location_level == 'COUNTRY':
                if start_year == end_year:
                    cursor.execute(sql_get_moh_data_one_year(start_year, start_week, end_week))
                else:
                    cursor.execute(sql_get_moh_data(start_year, start_week, end_year, end_week))

            else:
                if start_year == end_year:
                    cursor.execute(sql_get_data_by_filter_one_year(start_year, start_week, end_week, location_level, location_id))
                else:
                    cursor.execute(sql_get_data_by_filter(start_year, start_week, end_year, end_week, location_level, location_id))

            rows = cursor.fetchall()
            for row in rows:
                response.append(get_comment_info(row))

        return Response(response, status=status.HTTP_200_OK)

    except IllegalArgumentException as e:
        return Response(e.error_message, status=e.status_code)

    except Exception as e:
        return Response('Error: %s' % e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_comment_info(row):
    province = row[0] if row[0] else ' '
    district = row[1] if row[1] else ' '
    facility = row[2] if row[2] else ' '
    week = row[4].strftime('%Y') + 'W' + str(row[5])

    return {'province': province,
            'district': district,
            'facility': facility,
            'comment': row[3],
            'week': week}


def check_params(parameters):
    start_year = parameters.get(START).split('W')[0]
    start_week = parameters.get(START).split('W')[1]
    end_year = parameters.get(END).split('W')[0]
    end_week = parameters.get(END).split('W')[1]
    location = parameters.get(LOCATION)

    if not (start_year and start_week and end_year and end_week and location):
        raise IllegalArgumentException(message='%s, %s, %s, %s, %s are mandatory.' % (start_year, start_week, end_year, end_week, location))

    return start_year, start_week, end_year, end_week, location
