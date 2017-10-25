from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

import io
import xlsxwriter
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse

from dsd.exceptions.illegal_arguments_exception import IllegalArgumentException
from dsd.services.submission_service import START_DAY, END_DAY, LOCATION, INDEX_PAGE, fetch_ou_id_by_ou_uid
from dsd.services.export_excel_service import create_excel

PATH = '/tmp/'


@csrf_exempt
@api_view(['GET', ])
@renderer_classes((JSONRenderer,))
def data_submission_excel_endpoint(request):
    try:
        start, end, ou, page_index = check_params(request.GET)
        location_level, location_id = fetch_ou_id_by_ou_uid(ou)
        start_day = datetime.fromtimestamp(float(start) / 1000).strftime('%Y-%m-%d')
        end_day = datetime.fromtimestamp(float(end) / 1000).strftime('%Y-%m-%d')

        file_name = 'TodasSubmicoes' + start_day + '-' + end_day + '.xlsx'
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Todas Submicoes')
        create_excel(workbook, worksheet, location_level, location_id, start_day, end_day)

        output.seek(0)
        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=" % file_name

        return Response(response, status=status.HTTP_200_OK)

    except IllegalArgumentException as e:
        return Response(e.error_message, status=e.status_code)

    except Exception as e:
        return Response('Error: %s' % e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def file_iterator(file_name, chunk_size=512):
    with open(file_name) as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


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
